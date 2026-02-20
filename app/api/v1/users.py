"""
AGM Store Builder - User Endpoints

User profile management endpoints.
"""

from fastapi import APIRouter, status

from app.api.deps import DatabaseSession, CurrentUserId
from app.services.user_service import UserService
from app.schemas.user import (
    UserResponse,
    UpdateProfileRequest,
    ChangePasswordRequest,
    UserProfileResponse,
)
from app.schemas.common import MessageResponse

router = APIRouter()


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user(
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Get the authenticated user's profile.
    
    Returns complete user profile information.
    """
    user_service = UserService(db)
    user = await user_service.get_user_profile(user_id)
    
    return {
        "success": True,
        "data": user,
    }


@router.put("/me", response_model=UserProfileResponse)
async def update_profile(
    request: UpdateProfileRequest,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Update the authenticated user's profile.
    
    Updates user profile fields like name and phone.
    """
    user_service = UserService(db)
    user = await user_service.update_profile(
        user_id=user_id,
        full_name=request.full_name,
        phone=request.phone,
    )
    
    return {
        "success": True,
        "data": user,
        "message": "Profile updated successfully",
    }


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    request: ChangePasswordRequest,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Change the authenticated user's password.
    
    Requires current password verification.
    """
    user_service = UserService(db)
    await user_service.change_password(
        user_id=user_id,
        current_password=request.currentPassword,
        new_password=request.newPassword,
    )
    
    return {
        "success": True,
        "message": "Password changed successfully",
    }


@router.delete("/me", response_model=MessageResponse)
async def delete_account(
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Delete the authenticated user's account.
    
    Performs a soft delete, preserving data for potential recovery.
    """
    user_service = UserService(db)
    await user_service.delete_account(user_id)
    
    return {
        "success": True,
        "message": "Account deleted successfully",
    }
