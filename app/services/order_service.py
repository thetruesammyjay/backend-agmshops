"""
AGM Store Builder - Order Service

Business logic for order management.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.core.config import settings
from app.core.constants import ORDER_STATUS_TRANSITIONS, OrderStatus
from app.core.exceptions import NotFoundError, AuthorizationError, BadRequestError
from app.repositories.order_repository import OrderRepository
from app.repositories.store_repository import StoreRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.payment_repository import PaymentRepository
from app.services.monnify_service import MonnifyService


class OrderService:
    """Order service for order management operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.store_repo = StoreRepository(db)
        self.product_repo = ProductRepository(db)
        self.payment_repo = PaymentRepository(db)
        self.monnify = MonnifyService()
    
    async def create_order(
        self,
        store_username: str,
        customer_name: str,
        customer_phone: str,
        delivery_address: str,
        delivery_state: str,
        items: List[Dict[str, Any]],
        customer_email: Optional[str] = None,
        delivery_lga: Optional[str] = None,
        notes: Optional[str] = None,
        discount: float = 0,
        shipping_fee: float = 0,
    ) -> Dict[str, Any]:
        """Create a new order with payment initialization."""
        # Get store
        store = await self.store_repo.get_by_username(store_username)
        if not store or not store.is_active:
            raise NotFoundError(message="Store not found", resource_type="Store")
        
        # Process items and calculate totals
        order_items = []
        subtotal = 0
        
        for item in items:
            product = await self.product_repo.get_by_id(item["product_id"])
            if not product or product.store_id != store.id:
                raise BadRequestError(message=f"Product not found: {item['product_id']}")
            
            if not product.is_active:
                raise BadRequestError(message=f"Product is not available: {product.name}")
            
            if product.stock_quantity < item["quantity"]:
                raise BadRequestError(
                    message=f"Insufficient stock for {product.name}",
                    details={"available": product.stock_quantity},
                )
            
            item_subtotal = float(product.price) * item["quantity"]
            subtotal += item_subtotal
            
            order_items.append({
                "product_id": product.id,
                "product_name": product.name,
                "product_image": product.images[0] if product.images else None,
                "product_price": float(product.price),
                "quantity": item["quantity"],
                "subtotal": item_subtotal,
                "variant_selection": item.get("variant_selection"),
            })
        
        # Calculate AGM fee and total
        agm_fee = subtotal * (settings.AGM_FEE_PERCENTAGE / 100)
        total = subtotal - discount + shipping_fee + agm_fee
        
        # Generate order number
        order_number = await self.order_repo.generate_order_number()
        
        # Create order (items are stored as JSON in the Order model)
        order = await self.order_repo.create(
            store_id=store.id,
            order_number=order_number,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            delivery_address=delivery_address,
            delivery_state=delivery_state,
            delivery_lga=delivery_lga,
            items=order_items,  # JSON field
            subtotal=subtotal,
            discount=discount,
            shipping_fee=shipping_fee,
            agm_fee=agm_fee,
            total=total,
            notes=notes,
        )
        
        # Initialize payment with Monnify
        payment_data = await self.monnify.create_payment(
            order_id=order.id,
            user_id=store.user_id,
            amount=total,
            customer_name=customer_name,
            customer_email=customer_email,
        )
        
        # Save payment record to database
        await self.payment_repo.create(
            order_id=order.id,
            amount=total,
            currency="NGN",
            status="pending",
            payment_reference=payment_data["payment_reference"],
            monnify_reference=payment_data.get("transaction_reference"),
            transaction_reference=payment_data.get("transaction_reference"),
            checkout_url=payment_data.get("checkout_url"),
            account_number=payment_data["accountDetails"]["accountNumber"],
            account_name=payment_data["accountDetails"]["accountName"],
            bank_name=payment_data["accountDetails"]["bankName"],
            expires_at=datetime.fromisoformat(payment_data["expires_at"]) if payment_data.get("expires_at") else None,
        )
        
        # Decrement stock
        for item in order_items:
            await self.product_repo.update_stock(
                item["product_id"],
                item["quantity"],
                "decrement",
            )
        
        logger.info(f"Order created: {order_number}")
        
        return {
            "order": self._order_to_dict(order),
            "items": order_items,  # Items are already in dict format
            "payment": payment_data,
        }
    
    async def get_order_details(self, order_id: str, user_id: str) -> Dict[str, Any]:
        """Get order details (owner only)."""
        order = await self.order_repo.get_with_details(order_id)
        if not order:
            raise NotFoundError(message="Order not found", resource_type="Order")
        
        # Verify ownership through store
        store = await self.store_repo.get_by_id(order.store_id)
        if not store or store.user_id != user_id:
            raise AuthorizationError(message="You don't have access to this order")
        
        return {
            "order": self._order_to_dict(order),
            "items": order.items,  # Items are stored as JSON
            "payment": self._payment_to_dict(order.payment) if order.payment else None,
        }
    
    async def track_order(self, order_number: str) -> Dict[str, Any]:
        """Track order by order number (public)."""
        order = await self.order_repo.get_by_order_number(order_number)
        if not order:
            raise NotFoundError(message="Order not found", resource_type="Order")
        
        # Build tracking history
        tracking_history = [
            {"status": "pending", "timestamp": str(order.created_at)},
        ]
        
        # Add subsequent statuses based on current status
        status_order = ["confirmed", "processing", "shipped", "delivered", "fulfilled"]
        current_idx = status_order.index(order.status) if order.status in status_order else -1
        
        return {
            "order_number": order.order_number,
            "status": order.status,
            "payment_status": order.payment_status,
            "customer_name": order.customer_name,
            "total": float(order.total),
            "created_at": str(order.created_at),
            "items": order.items,  # Items are stored as JSON
            "tracking_history": tracking_history,
        }
    
    async def get_user_orders(
        self,
        user_id: str,
        store_id: Optional[str] = None,
        status: Optional[str] = None,
        payment_status: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get all orders for user's stores."""
        return await self.order_repo.get_user_orders(
            user_id=user_id,
            store_id=store_id,
            status=status,
            payment_status=payment_status,
            page=page,
            limit=limit,
            search=search,
            date_from=date_from,
            date_to=date_to,
        )
    
    async def update_order_status(
        self,
        order_id: str,
        user_id: str,
        new_status: str,
    ) -> Dict[str, Any]:
        """Update order status."""
        order = await self.order_repo.get_with_details(order_id)
        if not order:
            raise NotFoundError(message="Order not found", resource_type="Order")
        
        # Verify ownership
        store = await self.store_repo.get_by_id(order.store_id)
        if not store or store.user_id != user_id:
            raise AuthorizationError(message="You don't have access to this order")
        
        # Validate status transition
        current_status = OrderStatus(order.status)
        allowed = ORDER_STATUS_TRANSITIONS.get(current_status, [])
        
        if new_status not in [s.value for s in allowed]:
            raise BadRequestError(
                message=f"Cannot transition from {order.status} to {new_status}"
            )
        
        order = await self.order_repo.update_status(order_id, new_status)
        
        logger.info(f"Order status updated: {order_id} -> {new_status}")
        
        if order is None:
            raise NotFoundError(message="Order not found", resource_type="Order")
        
        return {
            "order": self._order_to_dict(order),
            "items": order.items,  # Items are stored as JSON
            "payment": self._payment_to_dict(order.payment) if order.payment else None,
        }
    
    async def cancel_order(self, order_id: str, user_id: str) -> None:
        """Cancel an order."""
        order = await self.order_repo.get_with_details(order_id)
        if not order:
            raise NotFoundError(message="Order not found", resource_type="Order")
        
        # Verify ownership
        store = await self.store_repo.get_by_id(order.store_id)
        if not store or store.user_id != user_id:
            raise AuthorizationError(message="You don't have access to this order")
        
        if not order.is_cancellable:
            raise BadRequestError(message="Order cannot be cancelled")
        
        # Restore stock from JSON items
        for item in order.items:
            await self.product_repo.update_stock(
                item["product_id"],
                item["quantity"],
                "increment",
            )
        
        await self.order_repo.update_status(order_id, "cancelled")
        logger.info(f"Order cancelled: {order_id}")
    
    def _order_to_dict(self, order) -> Dict[str, Any]:
        """Convert order model to dictionary."""
        return {
            "id": order.id,
            "order_number": order.order_number,
            "store_id": order.store_id,
            "customer_name": order.customer_name,
            "customer_email": order.customer_email,
            "customer_phone": order.customer_phone,
            "delivery_address": order.delivery_address,
            "delivery_state": order.delivery_state,
            "delivery_lga": order.delivery_lga,
            "subtotal": float(order.subtotal),
            "discount": float(order.discount),
            "shipping_fee": float(order.shipping_fee),
            "agm_fee": float(order.agm_fee),
            "total": float(order.total),
            "status": order.status,
            "payment_status": order.payment_status,
            "notes": order.notes,
            "created_at": str(order.created_at),
            "updated_at": str(order.updated_at) if order.updated_at else None,
        }
    
    def _item_to_dict(self, item) -> Dict[str, Any]:
        """Convert order item to dictionary."""
        return {
            "id": item.id,
            "product_id": item.product_id,
            "product_name": item.product_name,
            "product_image": item.product_image,
            "product_price": float(item.product_price),
            "quantity": item.quantity,
            "subtotal": float(item.subtotal),
            "variant_selection": item.variant_selection,
        }
    
    def _payment_to_dict(self, payment) -> Dict[str, Any]:
        """Convert payment to dictionary."""
        return {
            "id": payment.id,
            "payment_reference": payment.payment_reference,
            "amount": float(payment.amount),
            "status": payment.status,
            "accountDetails": {
                "accountNumber": payment.account_number,
                "accountName": payment.account_name,
                "bankName": payment.bank_name,
                "amount": float(payment.amount),
            } if payment.account_number else None,
            "paid_at": str(payment.paid_at) if payment.paid_at else None,
            "expires_at": str(payment.expires_at) if payment.expires_at else None,
            "created_at": str(payment.created_at),
        }
