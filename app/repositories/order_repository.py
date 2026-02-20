"""
AGM Store Builder - Order Repository

Data access layer for order operations.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy import select, func, update, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order
from app.models.store import Store
from app.models.payment import Payment
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """Repository for order data operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, Order)
    
    async def get_by_order_number(self, order_number: str) -> Optional[Order]:
        """Get order by order number."""
        result = await self.db.execute(
            select(Order)
            .options(
                selectinload(Order.payment),
            )
            .where(Order.order_number == order_number)
        )
        return result.scalar_one_or_none()
    
    async def get_with_details(self, order_id: str) -> Optional[Order]:
        """Get order with payment details. Items are stored as JSON in Order.items."""
        result = await self.db.execute(
            select(Order)
            .options(
                selectinload(Order.payment),
            )
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()
    
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
        """Get all orders for a user's stores."""
        query = (
            select(Order, Store.display_name.label("store_name"))
            .join(Store, Order.store_id == Store.id)
            .where(
                Store.user_id == user_id,
                Order.deleted_at.is_(None),
            )
        )
        
        if store_id:
            query = query.where(Order.store_id == store_id)
        
        if status:
            query = query.where(Order.status == status)
        
        if payment_status:
            query = query.where(Order.payment_status == payment_status)
        
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    Order.order_number.ilike(search_term),
                    Order.customer_name.ilike(search_term),
                    Order.customer_email.ilike(search_term),
                )
            )
        
        if date_from:
            query = query.where(Order.created_at >= date_from)
        
        if date_to:
            query = query.where(Order.created_at <= date_to)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0
        
        # Apply pagination
        offset = (page - 1) * limit
        query = query.order_by(Order.created_at.desc()).offset(offset).limit(limit)
        
        result = await self.db.execute(query)
        rows = result.all()
        
        orders = []
        for row in rows:
            order = row[0]
            store_name = row[1]
            orders.append({
                "id": order.id,
                "order_number": order.order_number,
                "store_id": order.store_id,
                "store_name": store_name,
                "customer_name": order.customer_name,
                "customer_email": order.customer_email,
                "customer_phone": order.customer_phone,
                "total": float(order.total),
                "status": order.status,
                "payment_status": order.payment_status,
                "created_at": str(order.created_at),
            })
        
        return {
            "orders": orders,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit,
                "hasMore": offset + len(orders) < total,
            },
        }
    
    async def generate_order_number(self) -> str:
        """Generate a unique order number."""
        import random
        now = datetime.now(timezone.utc)
        date_part = now.strftime("%Y%m%d")
        random_part = random.randint(10000, 99999)
        return f"ORD-{date_part}-{random_part}"
    
    async def update_status(
        self,
        order_id: str,
        new_status: str,
    ) -> Optional[Order]:
        """Update order status."""
        await self.db.execute(
            update(Order)
            .where(Order.id == order_id)
            .values(status=new_status)
        )
        await self.db.commit()
        return await self.get_by_id(order_id)
    
    async def update_payment_status(
        self,
        order_id: str,
        payment_status: str,
    ) -> None:
        """Update order payment status."""
        await self.db.execute(
            update(Order)
            .where(Order.id == order_id)
            .values(payment_status=payment_status)
        )
        await self.db.commit()
    
    async def get_store_orders_count(self, store_id: str) -> int:
        """Get total orders count for a store."""
        result = await self.db.execute(
            select(func.count(Order.id)).where(
                Order.store_id == store_id,
                Order.deleted_at.is_(None),
            )
        )
        return result.scalar() or 0
    
    async def get_store_revenue(self, store_id: str) -> float:
        """Get total revenue for a store (paid orders only)."""
        result = await self.db.execute(
            select(func.coalesce(func.sum(Order.total), 0)).where(
                Order.store_id == store_id,
                Order.payment_status == 'paid',
                Order.deleted_at.is_(None),
            )
        )
        return float(result.scalar() or 0)
