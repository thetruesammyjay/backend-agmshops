"""
AGM Store Builder - Authentication Service

Business logic for user authentication, registration, and token management.
"""

from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.core.security import (
    hash_password,
    verify_password,
    create_tokens,
    verify_refresh_token,
    create_password_reset_token,
    verify_password_reset_token,
)
from app.core.exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    OTPError,
    BadRequestError,
)
from app.repositories.user_repository import UserRepository
from app.services.otp_service import OTPService


class AuthService:
    """
    Authentication service handling user registration, login, and token management.
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.otp_service = OTPService(db)
    
    async def register(
        self,
        email: str,
        password: str,
        full_name: str,
        phone: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Register a new user.
        
        Args:
            email: User's email address
            password: Plain text password
            full_name: User's full name
            phone: Optional phone number
            
        Returns:
            User data and tokens
            
        Raises:
            ConflictError: If email already exists
        """
        # Check if email exists
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise ConflictError(message="Email already registered")
        
        # Check if phone exists
        if phone:
            existing_phone = await self.user_repo.get_by_phone(phone)
            if existing_phone:
                raise ConflictError(message="Phone number already registered")
        
        # Hash password
        password_hash = hash_password(password)
        
        # Create user
        user = await self.user_repo.create(
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            phone=phone,
        )
        
        # Create tokens
        tokens = create_tokens(user.id)
        
        # Send verification OTP
        await self.otp_service.send_email_verification(email)
        
        logger.info(f"User registered: {email}")
        
        return {
            "user": self._user_to_dict(user),
            "tokens": tokens,
        }
    
    async def login(
        self,
        email: str,
        password: str,
    ) -> Dict[str, Any]:
        """
        Authenticate a user with email and password.
        
        Args:
            email: User's email address
            password: Plain text password
            
        Returns:
            User data and tokens
            
        Raises:
            AuthenticationError: If credentials are invalid
        """
        # Get user
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise AuthenticationError(message="Invalid email or password")
        
        # Verify password
        if not verify_password(password, user.password_hash):
            raise AuthenticationError(message="Invalid email or password")
        
        # Check if user is active
        if not user.is_active:
            raise AuthenticationError(message="Account is deactivated")
        
        # Update last login
        await self.user_repo.update_last_login(user.id)
        
        # Create tokens
        tokens = create_tokens(user.id)
        
        logger.info(f"User logged in: {email}")
        
        return {
            "user": self._user_to_dict(user),
            "tokens": tokens,
        }
    
    async def refresh_tokens(self, refresh_token: str) -> Dict[str, str]:
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New access and refresh tokens
            
        Raises:
            AuthenticationError: If refresh token is invalid
        """
        try:
            user_id = verify_refresh_token(refresh_token)
        except Exception:
            raise AuthenticationError(message="Invalid refresh token")
        
        # Verify user exists and is active
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise AuthenticationError(message="User not found or inactive")
        
        # Create new tokens
        tokens = create_tokens(user_id)
        
        return tokens
    
    async def logout(self, user_id: str) -> None:
        """
        Logout a user by invalidating their tokens.
        
        Args:
            user_id: User's ID
        """
        # In a production system, you would:
        # - Add the tokens to a blacklist
        # - Revoke refresh tokens in the database
        logger.info(f"User logged out: {user_id}")
    
    async def send_password_reset_otp(self, email: str) -> None:
        """
        Send a password reset OTP to the user's email.
        
        Args:
            email: User's email address
            
        Raises:
            NotFoundError: If email is not registered
        """
        user = await self.user_repo.get_by_email(email)
        if not user:
            # For security, don't reveal if email exists
            logger.info(f"Password reset requested for non-existent email: {email}")
            return
        
        await self.otp_service.send_password_reset(email)
        logger.info(f"Password reset OTP sent to: {email}")
    
    async def verify_otp(
        self,
        email: str,
        otp: str,
        otp_type: str,
    ) -> Dict[str, Any]:
        """
        Verify an OTP code.
        
        Args:
            email: User's email address
            otp: OTP code to verify
            otp_type: Type of OTP (email, password_reset)
            
        Returns:
            Reset token for password reset, or user data for email verification
            
        Raises:
            OTPError: If OTP is invalid or expired
        """
        # Verify OTP
        is_valid = await self.otp_service.verify_otp(email, otp, otp_type)
        if not is_valid:
            raise OTPError(message="Invalid or expired OTP")
        
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise NotFoundError(message="User not found")
        
        result = {}
        
        if otp_type == "email":
            # Mark email as verified
            await self.user_repo.mark_email_verified(user.id)
            
            # Return user data and tokens for auto-login
            tokens = create_tokens(user.id)
            user = await self.user_repo.get_by_id(user.id)
            result = {
                "user": self._user_to_dict(user),
                "accessToken": tokens["accessToken"],
            }
        
        elif otp_type == "password_reset":
            # Create password reset token
            reset_token = create_password_reset_token(user.id)
            result = {
                "resetToken": reset_token,
                "expiresIn": "600",  # 10 minutes
            }
        
        logger.info(f"OTP verified for {email} ({otp_type})")
        return result
    
    async def reset_password(
        self,
        reset_token: str,
        new_password: str,
    ) -> None:
        """
        Reset user's password using verified reset token.
        
        Args:
            reset_token: Password reset token
            new_password: New password
            
        Raises:
            AuthenticationError: If reset token is invalid
        """
        try:
            user_id = verify_password_reset_token(reset_token)
        except Exception:
            raise AuthenticationError(message="Invalid or expired reset token")
        
        # Hash new password
        password_hash = hash_password(new_password)
        
        # Update password
        await self.user_repo.update_password(user_id, password_hash)
        
        logger.info(f"Password reset for user: {user_id}")
    
    async def resend_verification_otp(self, email: str) -> None:
        """
        Resend email verification OTP.
        
        Args:
            email: User's email address
        """
        user = await self.user_repo.get_by_email(email)
        if not user:
            # For security, don't reveal if email exists
            return
        
        if user.email_verified:
            raise BadRequestError(message="Email is already verified")
        
        await self.otp_service.send_email_verification(email)
        logger.info(f"Verification OTP resent to: {email}")
    
    def _user_to_dict(self, user) -> Dict[str, Any]:
        """Convert user model to dictionary."""
        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "email_verified": user.email_verified,
            "phone_verified": user.phone_verified,
            "is_active": user.is_active,
            "has_completed_onboarding": user.has_completed_onboarding,
            "last_login_at": str(user.last_login_at) if user.last_login_at else None,
            "created_at": str(user.created_at),
        }
