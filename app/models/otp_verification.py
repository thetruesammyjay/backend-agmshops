"""
AGM Store Builder - OTP Verification Model

SQLAlchemy model for the otp_verifications table.
"""

from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class OTPVerification(Base):
    """OTPVerification model for email/phone verification codes."""
    
    __tablename__ = "otp_verifications"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, index=True)
    code: Mapped[str] = mapped_column(String(6), nullable=False, index=True)
    otp_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        default=lambda: datetime.now(timezone.utc)
    )
    
    def __repr__(self) -> str:
        return f"<OTPVerification(id={self.id}, type={self.otp_type})>"
