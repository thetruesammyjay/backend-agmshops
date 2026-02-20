"""
AGM Store Builder - Refund Model

SQLAlchemy model for the refunds table.
"""

from typing import Optional, Any, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, DECIMAL, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.payment import Payment
    from app.models.order import Order


class Refund(Base, TimestampMixin):
    """Refund model representing the refunds table."""
    
    __tablename__ = "refunds"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    payment_id: Mapped[str] = mapped_column(String(36), ForeignKey("payments.id", ondelete="CASCADE"), nullable=False, index=True)
    order_id: Mapped[str] = mapped_column(String(36), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default='NGN', nullable=False)
    status: Mapped[str] = mapped_column(String(20), default='pending', nullable=False, index=True)
    refund_reference: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    monnify_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, unique=True, index=True)
    
    # Refund details
    reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    refund_type: Mapped[str] = mapped_column(String(20), default='full', nullable=False)  # full, partial
    customer_note: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    
    # Additional metadata from Monnify
    refund_metadata: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Status tracking
    initiated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    failed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    failure_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Relationships
    payment: Mapped["Payment"] = relationship("Payment", back_populates="refunds")
    order: Mapped["Order"] = relationship("Order", back_populates="refunds")
    
    def __repr__(self) -> str:
        return f"<Refund(id={self.id}, reference={self.refund_reference})>"
    
    @property
    def is_completed(self) -> bool:
        """Check if refund is completed."""
        return self.status == 'completed'
    
    @property
    def is_failed(self) -> bool:
        """Check if refund has failed."""
        return self.status == 'failed'
    
    @property
    def is_pending(self) -> bool:
        """Check if refund is pending."""
        return self.status == 'pending'
