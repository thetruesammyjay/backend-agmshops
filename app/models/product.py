"""
AGM Store Builder - Product Model

SQLAlchemy model for the products table.
"""

from typing import Optional, Any, TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, Text, Boolean, Integer, DECIMAL, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.store import Store


class Product(Base, TimestampMixin, SoftDeleteMixin):
    """Product model representing the products table."""
    
    __tablename__ = "products"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    store_id: Mapped[str] = mapped_column(String(36), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    compare_at_price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(12, 2), nullable=True)
    cost_price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(12, 2), nullable=True)
    sku: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    barcode: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False, index=True)
    low_stock_threshold: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    weight: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), nullable=True)
    dimensions: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    images: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    variations: Mapped[Optional[list[dict[str, Any]]]] = mapped_column(JSON, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    tags: Mapped[Optional[list[str]]] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Relationships
    store: Mapped["Store"] = relationship("Store", back_populates="products")
    
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name={self.name})>"
    
    @property
    def is_in_stock(self) -> bool:
        """Check if product is in stock."""
        return self.stock_quantity > 0
    
    @property
    def is_low_stock(self) -> bool:
        """Check if product is low on stock."""
        return self.stock_quantity <= self.low_stock_threshold
