"""
AGM Store Builder - Bank Account Model

SQLAlchemy model for the bank_accounts table.
"""

from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class BankAccount(Base, TimestampMixin):
    """BankAccount model representing the bank_accounts table."""
    
    __tablename__ = "bank_accounts"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    account_number: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    account_name: Mapped[str] = mapped_column(String(255), nullable=False)
    bank_code: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    bank_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Unique constraint for user + account + bank
    __table_args__ = (
        UniqueConstraint('user_id', 'account_number', 'bank_code', name='unique_account'),
    )
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="bank_accounts")
    
    def __repr__(self) -> str:
        return f"<BankAccount(id={self.id}, account_number={self.account_number})>"
