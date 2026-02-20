"""
AGM Store Builder - User Service

Business logic for user profile management.
"""

from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.core.security import hash_password, verify_password
from app.core.exceptions import NotFoundError, BadRequestError, AuthenticationError
from app.repositories.user_repository import UserRepository


class UserService:
    """User service for profile management operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
    
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Get user profile by ID.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            User profile data
            
        Raises:
            NotFoundError: If user not found
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError(message="User not found", resource_type="User")
        
        return self._user_to_dict(user)
    
    async def update_profile(
        self,
        user_id: str,
        full_name: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update user profile.
        
        Args:
            user_id: User's unique identifier
            full_name: New full name
            phone: New phone number
            
        Returns:
            Updated user profile
            
        Raises:
            NotFoundError: If user not found
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError(message="User not found", resource_type="User")
        
        updates = {}
        if full_name is not None:
            updates["full_name"] = full_name
        if phone is not None:
            updates["phone"] = phone
        
        if updates:
            user = await self.user_repo.update(user_id, **updates)
        
        logger.info(f"User profile updated: {user_id}")
        return self._user_to_dict(user)
    
    async def change_password(
        self,
        user_id: str,
        current_password: str,
        new_password: str,
    ) -> None:
        """
        Change user's password.
        
        Args:
            user_id: User's unique identifier
            current_password: Current password for verification
            new_password: New password to set
            
        Raises:
            NotFoundError: If user not found
            AuthenticationError: If current password is wrong
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError(message="User not found", resource_type="User")
        
        # Verify current password
        if not verify_password(current_password, user.password_hash):
            raise AuthenticationError(message="Current password is incorrect")
        
        # Hash and update new password
        new_hash = hash_password(new_password)
        await self.user_repo.update_password(user_id, new_hash)
        
        logger.info(f"Password changed for user: {user_id}")
    
    async def delete_account(self, user_id: str) -> None:
        """
        Delete user account (soft delete).
        
        Args:
            user_id: User's unique identifier
            
        Raises:
            NotFoundError: If user not found
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError(message="User not found", resource_type="User")
        
        await self.user_repo.soft_delete(user_id)
        logger.info(f"User account deleted: {user_id}")
    
    async def complete_onboarding(self, user_id: str) -> Dict[str, Any]:
        """
        Mark user as having completed onboarding.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            Updated user profile
        """
        user = await self.user_repo.update(user_id, has_completed_onboarding=True)
        if not user:
            raise NotFoundError(message="User not found", resource_type="User")
        
        logger.info(f"User completed onboarding: {user_id}")
        return self._user_to_dict(user)
    
    def _user_to_dict(self, user) -> Dict[str, Any]:
        """Convert user model to dictionary."""
        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "avatar_url": user.avatar_url,
            "email_verified": user.email_verified,
            "phone_verified": user.phone_verified,
            "is_active": user.is_active,
            "has_completed_onboarding": user.has_completed_onboarding,
            "last_login_at": str(user.last_login_at) if user.last_login_at else None,
            "created_at": str(user.created_at),
        }
