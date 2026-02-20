"""
AGM Store Builder - Payment Model

SQLAlchemy model for the payments table.
"""

from typing import Optional, Any, TYPE_CHECKING, List
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, DECIMAL, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.order import Order
    from app.models.refund import Refund


class Payment(Base, TimestampMixin):
    """Payment model representing the payments table."""
    
    __tablename__ = "payments"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    order_id: Mapped[str] = mapped_column(String(36), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default='NGN', nullable=False)
    status: Mapped[str] = mapped_column(String(20), default='pending', nullable=False, index=True)
    payment_method: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    payment_reference: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    monnify_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, unique=True, index=True)
    transaction_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    checkout_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    account_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    account_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    bank_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    payment_metadata: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="payment")
    refunds: Mapped[List["Refund"]] = relationship("Refund", back_populates="payment", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Payment(id={self.id}, reference={self.payment_reference})>"
    
    @property
    def is_paid(self) -> bool:
        """Check if payment is completed."""
        return self.status == 'paid'
    
    @property
    def is_expired(self) -> bool:
        """Check if payment has expired."""
        return self.status == 'expired'
