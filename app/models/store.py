"""
AGM Store Builder - Store Model

SQLAlchemy model for the stores table.
"""

from typing import Optional, Any, TYPE_CHECKING
from sqlalchemy import String, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.product import Product
    from app.models.order import Order


class Store(Base, TimestampMixin, SoftDeleteMixin):
    """Store model representing the stores table."""
    
    __tablename__ = "stores"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    banner_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    template_id: Mapped[str] = mapped_column(String(20), default='products', nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    custom_colors: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    custom_fonts: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    social_links: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="stores")
    products: Mapped[list["Product"]] = relationship("Product", back_populates="store", lazy="dynamic")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="store", lazy="dynamic")
    
    def __repr__(self) -> str:
        return f"<Store(id={self.id}, username={self.username})>"
