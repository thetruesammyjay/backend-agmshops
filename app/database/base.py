"""
AGM Store Builder - Base Database Model

Base SQLAlchemy model with common mixins for all database models.
"""

from datetime import datetime, timezone
from typing import Any, Optional
from sqlalchemy import Column, DateTime, Boolean, String, text
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamp columns."""
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=text("CURRENT_TIMESTAMP"),
    )
    
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
        server_onupdate=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )


class SoftDeleteMixin:
    """Mixin that adds soft delete functionality."""
    
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        default=None,
        index=True,
    )
    
    @property
    def is_deleted(self) -> bool:
        """Check if the record is soft-deleted."""
        return self.deleted_at is not None
    
    def soft_delete(self) -> None:
        """Mark the record as soft-deleted."""
        self.deleted_at = datetime.now(timezone.utc)
    
    def restore(self) -> None:
        """Restore a soft-deleted record."""
        self.deleted_at = None


class BaseModel(Base, TimestampMixin, SoftDeleteMixin):
    """
    Base model with UUID primary key, timestamps, and soft delete.
    
    Use this as the base for most entities.
    """
    
    __abstract__ = True
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    
    def to_dict(self, exclude: Optional[list[str]] = None) -> dict[str, Any]:
        """
        Convert model to dictionary.
        
        Args:
            exclude: List of field names to exclude
            
        Returns:
            Dictionary representation of the model
        """
        exclude = exclude or []
        result = {}
        
        for column in self.__table__.columns:
            if column.name in exclude:
                continue
            
            value = getattr(self, column.name)
            
            # Convert datetime to ISO format string
            if isinstance(value, datetime):
                value = value.isoformat()
            
            result[column.name] = value
        
        return result
    
    def __repr__(self) -> str:
        """String representation of the model."""
        class_name = self.__class__.__name__
        pk = getattr(self, 'id', None)
        return f"<{class_name}(id={pk})>"
