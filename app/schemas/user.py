"""
AGM Store Builder - User Schemas

Pydantic schemas for user-related requests and responses.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user data."""
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


class UserResponse(BaseModel):
    """User data response."""
    id: str
    email: str
    full_name: str
    phone: Optional[str] = None
    email_verified: bool = False
    phone_verified: bool = False
    is_active: bool = True
    has_completed_onboarding: bool = False


class UserProfileResponse(BaseModel):
    """User profile response."""
    success: bool = True
    data: UserBase
    message: Optional[str] = None


class UpdateProfileRequest(BaseModel):
    """Update user profile request."""
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    phone: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    """Change password request."""
    currentPassword: str
    newPassword: str = Field(min_length=8)
