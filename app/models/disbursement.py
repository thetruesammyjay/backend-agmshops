"""
AGM Store Builder - Disbursement Model

SQLAlchemy model for the disbursements table.
"""

from typing import Optional, Any, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, DECIMAL, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Disbursement(Base, TimestampMixin):
    """Disbursement model representing the disbursements table."""
    
    __tablename__ = "disbursements"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default='NGN', nullable=False)
    status: Mapped[str] = mapped_column(String(20), default='pending', nullable=False, index=True)
    reference: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    monnify_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, unique=True, index=True)
    
    # Bank details
    account_number: Mapped[str] = mapped_column(String(20), nullable=False)
    account_name: Mapped[str] = mapped_column(String(255), nullable=False)
    bank_code: Mapped[str] = mapped_column(String(10), nullable=False)
    bank_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Additional metadata from Monnify
    narration: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    fee: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(12, 2), nullable=True)
    disbursement_metadata: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Status tracking
    initiated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    failed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    failure_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="disbursements")
    
    def __repr__(self) -> str:
        return f"<Disbursement(id={self.id}, reference={self.reference})>"
    
    @property
    def is_completed(self) -> bool:
        """Check if disbursement is completed."""
        return self.status == 'completed'
    
    @property
    def is_failed(self) -> bool:
        """Check if disbursement has failed."""
        return self.status == 'failed'
    
    @property
    def is_pending(self) -> bool:
        """Check if disbursement is pending."""
        return self.status == 'pending'
