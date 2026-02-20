"""
AGM Store Builder - Payment Repository

Data access layer for payment operations.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment
from app.models.bank_account import BankAccount
from app.repositories.base import BaseRepository


class PaymentRepository(BaseRepository[Payment]):
    """Repository for payment data operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, Payment)
    
    async def get_by_reference(self, payment_reference: str) -> Optional[Payment]:
        """Get payment by payment reference."""
        result = await self.db.execute(
            select(Payment).where(Payment.payment_reference == payment_reference)
        )
        return result.scalar_one_or_none()
    
    async def get_by_monnify_reference(self, monnify_reference: str) -> Optional[Payment]:
        """Get payment by Monnify reference."""
        result = await self.db.execute(
            select(Payment).where(Payment.monnify_reference == monnify_reference)
        )
        return result.scalar_one_or_none()
    
    async def get_by_order(self, order_id: str) -> Optional[Payment]:
        """Get payment for an order."""
        result = await self.db.execute(
            select(Payment).where(Payment.order_id == order_id)
        )
        return result.scalar_one_or_none()
    
    async def update_status(
        self,
        payment_id: str,
        status: str,
        monnify_reference: Optional[str] = None,
        payment_method: Optional[str] = None,
    ) -> Optional[Payment]:
        """Update payment status."""
        values: Dict[str, Any] = {"status": status}
        
        if monnify_reference:
            values["monnify_reference"] = monnify_reference
        
        if payment_method:
            values["payment_method"] = payment_method
        
        if status == "paid":
            values["paid_at"] = datetime.now(timezone.utc)
        
        await self.db.execute(
            update(Payment)
            .where(Payment.id == payment_id)
            .values(**values)
        )
        await self.db.commit()
        
        return await self.get_by_id(payment_id)
    
    async def mark_expired(self, payment_id: str) -> None:
        """Mark payment as expired."""
        await self.db.execute(
            update(Payment)
            .where(Payment.id == payment_id)
            .values(status="expired")
        )
        await self.db.commit()


class BankAccountRepository(BaseRepository[BankAccount]):
    """Repository for bank account operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, BankAccount)
    
    async def get_by_user(self, user_id: str) -> List[BankAccount]:
        """Get all bank accounts for a user."""
        result = await self.db.execute(
            select(BankAccount).where(
                BankAccount.user_id == user_id,
            ).order_by(BankAccount.is_primary.desc(), BankAccount.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def get_primary(self, user_id: str) -> Optional[BankAccount]:
        """Get user's primary bank account."""
        result = await self.db.execute(
            select(BankAccount).where(
                BankAccount.user_id == user_id,
                BankAccount.is_primary == True,
            )
        )
        return result.scalar_one_or_none()
    
    async def set_primary(self, account_id: str, user_id: str) -> Optional[BankAccount]:
        """Set a bank account as primary."""
        # First, unset all primary flags for user
        await self.db.execute(
            update(BankAccount)
            .where(BankAccount.user_id == user_id)
            .values(is_primary=False)
        )
        
        # Set the specified account as primary
        await self.db.execute(
            update(BankAccount)
            .where(
                BankAccount.id == account_id,
                BankAccount.user_id == user_id,
            )
            .values(is_primary=True)
        )
        await self.db.commit()
        
        return await self.get_by_id(account_id)
    
    async def account_exists(
        self,
        user_id: str,
        account_number: str,
        bank_code: str,
    ) -> bool:
        """Check if account already exists for user."""
        result = await self.db.execute(
            select(BankAccount.id).where(
                BankAccount.user_id == user_id,
                BankAccount.account_number == account_number,
                BankAccount.bank_code == bank_code,
            )
        )
        return result.scalar_one_or_none() is not None
