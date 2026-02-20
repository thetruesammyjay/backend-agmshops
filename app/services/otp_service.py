"""
AGM Store Builder - OTP Service

OTP generation, sending, and verification.
"""

import random
import string
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.core.config import settings
from app.core.constants import OTPType


class OTPService:
    """
    OTP service for generating, sending, and verifying OTP codes.
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def generate_otp(self, length: int = 6) -> str:
        """Generate a random numeric OTP code."""
        return ''.join(random.choices(string.digits, k=length))
    
    async def send_email_verification(self, email: str) -> None:
        """
        Send email verification OTP.
        
        In development, uses default OTP. In production, sends via email.
        """
        if settings.USE_DEFAULT_OTP:
            otp = settings.DEFAULT_OTP
        else:
            otp = self.generate_otp()
        
        # Store OTP in database (to be implemented with OTP model)
        await self._store_otp(email, otp, OTPType.EMAIL)
        
        if not settings.USE_DEFAULT_OTP:
            # Send via email service
            from app.services.email_service import EmailService
            email_service = EmailService()
            await email_service.send_otp(email, otp)
        
        logger.info(f"Verification OTP {'generated' if settings.USE_DEFAULT_OTP else 'sent'} for: {email}")
    
    async def send_password_reset(self, email: str) -> None:
        """
        Send password reset OTP.
        """
        if settings.USE_DEFAULT_OTP:
            otp = settings.DEFAULT_OTP
        else:
            otp = self.generate_otp()
        
        await self._store_otp(email, otp, OTPType.PASSWORD_RESET)
        
        if not settings.USE_DEFAULT_OTP:
            from app.services.email_service import EmailService
            email_service = EmailService()
            await email_service.send_password_reset_otp(email, otp)
        
        logger.info(f"Password reset OTP {'generated' if settings.USE_DEFAULT_OTP else 'sent'} for: {email}")
    
    async def verify_otp(
        self,
        email: str,
        otp: str,
        otp_type: str,
    ) -> bool:
        """
        Verify an OTP code.
        
        Args:
            email: User's email
            otp: OTP code to verify
            otp_type: Type of OTP
            
        Returns:
            True if valid, False otherwise
        """
        # In development with default OTP
        if settings.USE_DEFAULT_OTP and otp == settings.DEFAULT_OTP:
            return True
        
        # Verify from database (to be implemented)
        return await self._verify_stored_otp(email, otp, otp_type)
    
    async def _store_otp(
        self,
        email: str,
        otp: str,
        otp_type: OTPType,
    ) -> None:
        """Store OTP in database."""
        # This will use the OTP verification repository
        # For now, we rely on default OTP in development
        pass
    
    async def _verify_stored_otp(
        self,
        email: str,
        otp: str,
        otp_type: str,
    ) -> bool:
        """Verify OTP from database."""
        # This will use the OTP verification repository
        # For now, relies on default OTP
        return otp == settings.DEFAULT_OTP
