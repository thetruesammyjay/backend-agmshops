"""
AGM Store Builder - Payment Service

Business logic for payment processing with Monnify.
"""

from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.core.exceptions import NotFoundError, BadRequestError, ConflictError
from app.repositories.payment_repository import PaymentRepository, BankAccountRepository
from app.repositories.order_repository import OrderRepository
from app.services.monnify_service import MonnifyService


class PaymentService:
    """Payment service for payment operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.payment_repo = PaymentRepository(db)
        self.bank_repo = BankAccountRepository(db)
        self.order_repo = OrderRepository(db)
        self.monnify = MonnifyService()
    
    async def verify_payment(self, reference: str) -> Dict[str, Any]:
        """Verify payment status with Monnify."""
        payment = await self.payment_repo.get_by_reference(reference)
        if not payment:
            raise NotFoundError(message="Payment not found", resource_type="Payment")
        
        # Verify with Monnify
        monnify_status = await self.monnify.verify_payment(reference)
        
        # Update local status if changed
        if monnify_status["status"] != payment.status:
            await self.payment_repo.update_status(
                payment.id,
                monnify_status["status"],
                monnify_status.get("monnify_reference"),
                monnify_status.get("payment_method"),
            )
            
            # Update order payment status
            if monnify_status["status"] == "paid":
                await self.order_repo.update_payment_status(payment.order_id, "paid")
        
        order = await self.order_repo.get_by_id(payment.order_id)
        
        return {
            "verified": monnify_status["status"] == "paid",
            "status": monnify_status["status"],
            "payment": self._payment_to_dict(payment),
            "order": self._order_to_dict(order) if order else None,
        }
    
    async def get_payment_details(self, reference: str) -> Dict[str, Any]:
        """Get payment details by reference."""
        payment = await self.payment_repo.get_by_reference(reference)
        if not payment:
            raise NotFoundError(message="Payment not found", resource_type="Payment")
        
        return self._payment_to_dict(payment)
    
    async def reinitialize_payment(self, reference: str) -> Dict[str, Any]:
        """Reinitialize an expired payment."""
        payment = await self.payment_repo.get_by_reference(reference)
        if not payment:
            raise NotFoundError(message="Payment not found", resource_type="Payment")
        
        if payment.status == "paid":
            raise BadRequestError(message="Payment already completed")
        
        # Get order for amount
        order = await self.order_repo.get_by_id(payment.order_id)
        if not order:
            raise NotFoundError(message="Order not found", resource_type="Order")
        
        # Reinitialize with Monnify
        new_payment_data = await self.monnify.create_payment(
            order_id=order.id,
            user_id=payment.user_id,
            amount=float(order.total),
            customer_name=order.customer_name,
            customer_email=order.customer_email,
        )
        
        return new_payment_data
    
    async def process_successful_payment(
        self,
        payment_reference: str,
        monnify_reference: str,
        amount_paid: float,
        event_data: Dict[str, Any],
    ) -> None:
        """Process a successful payment webhook."""
        payment = await self.payment_repo.get_by_reference(payment_reference)
        if not payment:
            logger.warning(f"Payment not found for reference: {payment_reference}")
            return
        
        # Update payment status
        await self.payment_repo.update_status(
            payment.id,
            "paid",
            monnify_reference=monnify_reference,
            payment_method=event_data.get("paymentMethod"),
        )
        
        # Update order status
        await self.order_repo.update_payment_status(payment.order_id, "paid")
        
        logger.info(f"Payment successful: {payment_reference}")
    
    async def process_failed_payment(
        self,
        payment_reference: str,
        event_data: Dict[str, Any],
    ) -> None:
        """Process a failed payment webhook."""
        payment = await self.payment_repo.get_by_reference(payment_reference)
        if not payment:
            logger.warning(f"Payment not found for reference: {payment_reference}")
            return
        
        await self.payment_repo.update_status(payment.id, "failed")
        await self.order_repo.update_payment_status(payment.order_id, "failed")
        
        logger.info(f"Payment failed: {payment_reference}")
    
    async def process_expired_payment(
        self,
        payment_reference: str,
        event_data: Dict[str, Any],
    ) -> None:
        """Process an expired payment webhook."""
        payment = await self.payment_repo.get_by_reference(payment_reference)
        if not payment:
            logger.warning(f"Payment not found for reference: {payment_reference}")
            return
        
        await self.payment_repo.mark_expired(payment.id)
        await self.order_repo.update_payment_status(payment.order_id, "expired")
        
        logger.info(f"Payment expired: {payment_reference}")
    
    # Bank account methods
    async def add_bank_account(
        self,
        user_id: str,
        account_name: str,
        account_number: str,
        bank_code: str,
        bank_name: str,
    ) -> Dict[str, Any]:
        """Add a bank account for payouts."""
        # Check if account exists
        if await self.bank_repo.account_exists(user_id, account_number, bank_code):
            raise ConflictError(message="Bank account already exists")
        
        # Check if this is the first account (make it primary)
        existing = await self.bank_repo.get_by_user(user_id)
        is_primary = len(existing) == 0
        
        account = await self.bank_repo.create(
            user_id=user_id,
            account_name=account_name,
            account_number=account_number,
            bank_code=bank_code,
            bank_name=bank_name,
            is_primary=is_primary,
        )
        
        logger.info(f"Bank account added for user: {user_id}")
        return self._account_to_dict(account)
    
    async def resolve_bank_account(
        self,
        account_number: str,
        bank_code: str,
    ) -> Dict[str, Any]:
        """
        Resolve/verify a bank account number using Monnify API.
        
        In development, returns mock data. In production, calls Monnify API.
        """
        from app.utils.constants import NIGERIAN_BANKS
        
        # Get bank name from code
        bank_name = "Unknown Bank"
        for bank in NIGERIAN_BANKS:
            if bank["code"] == bank_code:
                bank_name = bank["name"]
                break
        
        # Use Monnify to validate bank account
        result = await self.monnify.validate_bank_account(
            account_number=account_number,
            bank_code=bank_code,
        )
        
        return {
            "account_name": result["account_name"],
            "account_number": result["account_number"],
            "bank_code": bank_code,
            "bank_name": bank_name,
        }
    
    async def get_user_bank_accounts(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all bank accounts for a user."""
        accounts = await self.bank_repo.get_by_user(user_id)
        return [self._account_to_dict(acc) for acc in accounts]
    
    async def set_primary_bank_account(
        self,
        account_id: str,
        user_id: str,
    ) -> Dict[str, Any]:
        """Set a bank account as primary."""
        account = await self.bank_repo.get_by_id(account_id)
        if not account or account.user_id != user_id:
            raise NotFoundError(message="Bank account not found")
        
        account = await self.bank_repo.set_primary(account_id, user_id)
        
        logger.info(f"Primary bank account set: {account_id}")
        return self._account_to_dict(account)
    
    async def delete_bank_account(self, account_id: str, user_id: str) -> None:
        """Delete a bank account."""
        account = await self.bank_repo.get_by_id(account_id)
        if not account or account.user_id != user_id:
            raise NotFoundError(message="Bank account not found")
        
        await self.bank_repo.delete(account_id)
        logger.info(f"Bank account deleted: {account_id}")
    
    def _payment_to_dict(self, payment) -> Dict[str, Any]:
        """Convert payment model to dictionary."""
        return {
            "id": payment.id,
            "order_id": payment.order_id,
            "payment_reference": payment.payment_reference,
            "monnify_reference": payment.monnify_reference,
            "amount": float(payment.amount),
            "status": payment.status,
            "payment_method": payment.payment_method,
            "accountDetails": {
                "accountNumber": payment.account_number,
                "accountName": payment.account_name or "",
                "bankName": payment.bank_name or "",
                "amount": float(payment.amount),
            } if payment.account_number else None,
            "paid_at": str(payment.paid_at) if payment.paid_at else None,
            "expires_at": str(payment.expires_at) if payment.expires_at else None,
            "created_at": str(payment.created_at),
        }
    
    def _order_to_dict(self, order) -> Dict[str, Any]:
        """Convert order to dictionary."""
        return {
            "id": order.id,
            "order_number": order.order_number,
            "total": float(order.total),
            "status": order.status,
            "payment_status": order.payment_status,
        }
    
    def _account_to_dict(self, account) -> Dict[str, Any]:
        """Convert bank account to dictionary."""
        return {
            "id": account.id,
            "user_id": account.user_id,
            "account_name": account.account_name,
            "account_number": account.account_number,
            "bank_code": account.bank_code,
            "bank_name": account.bank_name,
            "is_verified": account.is_verified,
            "is_primary": account.is_primary,
            "created_at": str(account.created_at),
        }
