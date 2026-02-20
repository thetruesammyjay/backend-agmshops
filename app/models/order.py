"""
AGM Store Builder - Order Model

SQLAlchemy model for the orders table.
"""

from typing import Optional, Any, TYPE_CHECKING, List
from decimal import Decimal
from sqlalchemy import String, Text, DECIMAL, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.store import Store
    from app.models.payment import Payment
    from app.models.refund import Refund


class Order(Base, TimestampMixin, SoftDeleteMixin):
    """Order model representing the orders table."""
    
    __tablename__ = "orders"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    store_id: Mapped[str] = mapped_column(String(36), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, index=True)
    order_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    customer_phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    customer_address: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    delivery_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    delivery_state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    delivery_lga: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    items: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False)  # Items stored as JSON
    subtotal: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    discount: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), default=0, nullable=False)
    shipping_fee: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), default=0, nullable=False)
    agm_fee: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), default=0, nullable=False)
    total: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default='pending', nullable=False, index=True)
    payment_status: Mapped[str] = mapped_column(String(20), default='pending', nullable=False, index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    store: Mapped["Store"] = relationship("Store", back_populates="orders")
    payment: Mapped[Optional["Payment"]] = relationship("Payment", back_populates="order", uselist=False)
    refunds: Mapped[List["Refund"]] = relationship("Refund", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Order(id={self.id}, order_number={self.order_number})>"
    
    @property
    def is_paid(self) -> bool:
        """Check if order is paid."""
        return self.payment_status == 'paid'
    
    @property
    def is_cancellable(self) -> bool:
        """Check if order can be cancelled."""
        return self.status in ['pending', 'confirmed']
