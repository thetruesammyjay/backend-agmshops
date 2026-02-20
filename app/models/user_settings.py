"""
AGM Store Builder - User Settings Model

SQLAlchemy model for the user_settings table.
"""

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class UserSettings(Base, TimestampMixin):
    """UserSettings model for user preferences."""
    
    __tablename__ = "user_settings"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    # Notification preferences
    email_notifications: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sms_notifications: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    order_notifications: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    payment_notifications: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    payout_notifications: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    marketing_notifications: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Privacy settings
    profile_visibility: Mapped[str] = mapped_column(String(20), default='public', nullable=False)
    show_email: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    show_phone: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Preferences
    default_currency: Mapped[str] = mapped_column(String(3), default='NGN', nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default='Africa/Lagos', nullable=False)
    language: Mapped[str] = mapped_column(String(10), default='en', nullable=False)
    
    # Security
    two_factor_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    login_alerts: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    def __repr__(self) -> str:
        return f"<UserSettings(id={self.id}, user_id={self.user_id})>"
