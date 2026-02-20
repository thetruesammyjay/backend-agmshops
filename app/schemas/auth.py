"""
AGM Store Builder - Authentication Schemas

Pydantic schemas for authentication requests and responses.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field, field_validator
import re

from app.core.constants import OTPType


class RegisterRequest(BaseModel):
    """User registration request."""
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=2, max_length=255)
    phone: Optional[str] = None
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        return v


class LoginRequest(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    """Token refresh request."""
    refreshToken: str


class ForgotPasswordRequest(BaseModel):
    """Password reset request."""
    email: EmailStr


class VerifyOTPRequest(BaseModel):
    """OTP verification request."""
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)
    type: str = Field(default="email")


class ResetPasswordRequest(BaseModel):
    """Password reset with token."""
    resetToken: str
    newPassword: str = Field(min_length=8)
    
    @field_validator("newPassword")
    @classmethod
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        return v


class ResendVerificationRequest(BaseModel):
    """Resend verification OTP request."""
    email: EmailStr


class TokenData(BaseModel):
    """JWT token data."""
    accessToken: str
    refreshToken: str


class UserData(BaseModel):
    """User data in response."""
    id: str
    email: str
    full_name: str
    phone: Optional[str] = None
    email_verified: bool = False
    phone_verified: bool = False
    is_active: bool = True
    has_completed_onboarding: bool = False
    last_login_at: Optional[str] = None
    created_at: str


class AuthResponseData(BaseModel):
    """Auth response data."""
    user: UserData
    tokens: TokenData


class AuthResponse(BaseModel):
    """Authentication response."""
    success: bool = True
    data: AuthResponseData
    message: Optional[str] = None


class TokenResponse(BaseModel):
    """Token refresh response."""
    success: bool = True
    data: TokenData


class MessageResponse(BaseModel):
    """Simple message response."""
    success: bool = True
    message: str


class VerifyOTPResponseData(BaseModel):
    """OTP verification response data."""
    resetToken: Optional[str] = None
    expiresIn: Optional[int] = None
    user: Optional[UserData] = None
    accessToken: Optional[str] = None


class VerifyOTPResponse(BaseModel):
    """OTP verification response."""
    success: bool = True
    data: VerifyOTPResponseData
    message: Optional[str] = None
