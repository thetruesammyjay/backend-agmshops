"""
AGM Store Builder - User Model

SQLAlchemy model for the users table.
"""

from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.store import Store
    from app.models.bank_account import BankAccount
    from app.models.disbursement import Disbursement


class User(Base, TimestampMixin, SoftDeleteMixin):
    """User model representing the users table."""
    
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True, index=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    role: Mapped[str] = mapped_column(String(20), default='user', nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    phone_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_completed_onboarding: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    stores: Mapped[list["Store"]] = relationship("Store", back_populates="user", lazy="dynamic")
    bank_accounts: Mapped[list["BankAccount"]] = relationship("BankAccount", back_populates="user", lazy="dynamic")
    disbursements: Mapped[List["Disbursement"]] = relationship("Disbursement", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
