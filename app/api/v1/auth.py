"""
AGM Store Builder - Authentication Endpoints

Handles user registration, login, logout, password reset, and OTP verification.
"""

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, EmailStr, Field

from app.api.deps import DatabaseSession, CurrentUserId
from app.core.security import create_tokens, verify_refresh_token, verify_password, hash_password
from app.core.exceptions import AuthenticationError, BadRequestError, NotFoundError
from app.services.auth_service import AuthService
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    VerifyOTPRequest,
    ResetPasswordRequest,
    ResendVerificationRequest,
    AuthResponse,
    TokenResponse,
    MessageResponse,
    VerifyOTPResponse,
)

router = APIRouter()


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
    db: DatabaseSession,
):
    """
    Register a new user account.
    
    Creates a new user with the provided email and password.
    Returns user data and authentication tokens.
    """
    auth_service = AuthService(db)
    result = await auth_service.register(
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        phone=request.phone,
    )
    
    return {
        "success": True,
        "data": result,
        "message": "Registration successful",
    }


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    request: RegisterRequest,
    db: DatabaseSession,
):
    """
    Signup - alias for register.
    
    Creates a new user with the provided email and password.
    Returns user data and authentication tokens.
    """
    auth_service = AuthService(db)
    result = await auth_service.register(
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        phone=request.phone,
    )
    
    return {
        "success": True,
        "data": result,
        "message": "Registration successful",
    }


@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    db: DatabaseSession,
):
    """
    Login with email and password.
    
    Returns user data and authentication tokens.
    """
    auth_service = AuthService(db)
    result = await auth_service.login(
        email=request.email,
        password=request.password,
    )
    
    return {
        "success": True,
        "data": result,
        "message": "Login successful",
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: DatabaseSession,
):
    """
    Get new access token using refresh token.
    
    Returns a new access token and optionally a new refresh token.
    """
    auth_service = AuthService(db)
    result = await auth_service.refresh_tokens(request.refreshToken)
    
    return {
        "success": True,
        "data": result,
    }


@router.post("/logout", response_model=MessageResponse)
async def logout(
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Logout the current user.
    
    Invalidates the current session tokens.
    """
    auth_service = AuthService(db)
    await auth_service.logout(user_id)
    
    return {
        "success": True,
        "message": "Logged out successfully",
    }


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: DatabaseSession,
):
    """
    Request a password reset OTP.
    
    Sends an OTP code to the user's email.
    """
    auth_service = AuthService(db)
    await auth_service.send_password_reset_otp(request.email)
    
    return {
        "success": True,
        "message": "Password reset OTP sent to your email",
    }


@router.post("/verify-otp", response_model=VerifyOTPResponse)
async def verify_otp(
    request: VerifyOTPRequest,
    db: DatabaseSession,
):
    """
    Verify an OTP code.
    
    For email verification or password reset.
    Returns a reset token if for password reset.
    """
    auth_service = AuthService(db)
    result = await auth_service.verify_otp(
        email=request.email,
        otp=request.otp,
        otp_type=request.type,
    )
    
    return {
        "success": True,
        "data": result,
        "message": "OTP verified successfully",
    }


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    request: ResetPasswordRequest,
    db: DatabaseSession,
):
    """
    Reset password using verified reset token.
    
    Updates the user's password after OTP verification.
    """
    auth_service = AuthService(db)
    await auth_service.reset_password(
        reset_token=request.resetToken,
        new_password=request.newPassword,
    )
    
    return {
        "success": True,
        "message": "Password reset successful",
    }


@router.post("/resend-verification", response_model=MessageResponse)
async def resend_verification(
    request: ResendVerificationRequest,
    db: DatabaseSession,
):
    """
    Resend email verification OTP.
    
    Sends a new OTP code to verify the user's email.
    """
    auth_service = AuthService(db)
    await auth_service.resend_verification_otp(request.email)
    
    return {
        "success": True,
        "message": "Verification email sent",
    }
