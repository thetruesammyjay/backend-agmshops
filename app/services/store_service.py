"""
AGM Store Builder - Store Service

Business logic for store management.
"""

from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.core.exceptions import NotFoundError, ConflictError, AuthorizationError
from app.repositories.store_repository import StoreRepository


class StoreService:
    """Store service for store management operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.store_repo = StoreRepository(db)
    
    async def create_store(
        self,
        user_id: str,
        name: str,
        username: str,
        description: Optional[str] = None,
        category: Optional[str] = None,
        logo: Optional[str] = None,
        banner: Optional[str] = None,
        social_links: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new store.
        
        Args:
            user_id: Owner's user ID
            name: Store display name
            username: Unique store username
            description: Store description
            category: Store category
            logo: Logo URL
            banner: Banner URL
            social_links: Social media links
            
        Returns:
            Created store data
            
        Raises:
            ConflictError: If username already exists
        """
        # Check username availability
        username_lower = username.lower()
        if await self.store_repo.username_exists(username_lower):
            raise ConflictError(
                message="Username already taken",
                details={"username": username_lower},
            )
        
        store = await self.store_repo.create(
            user_id=user_id,
            username=username_lower,
            display_name=name,
            description=description,
            category=category,
            logo_url=logo,
            banner_url=banner,
            social_links=social_links,
        )
        
        logger.info(f"Store created: {store.id} by user {user_id}")
        return self._store_to_dict(store)
    
    async def get_store_by_id(self, store_id: str, user_id: str) -> Dict[str, Any]:
        """
        Get store by ID (owner only).
        
        Args:
            store_id: Store's unique identifier
            user_id: Requesting user's ID
            
        Returns:
            Store data
            
        Raises:
            NotFoundError: If store not found
            AuthorizationError: If user doesn't own the store
        """
        store = await self.store_repo.get_by_id(store_id)
        if not store:
            raise NotFoundError(message="Store not found", resource_type="Store")
        
        if store.user_id != user_id:
            raise AuthorizationError(message="You don't have access to this store")
        
        return self._store_to_dict(store)
    
    async def get_store_by_username(self, username: str) -> Dict[str, Any]:
        """
        Get public store by username.
        
        Args:
            username: Store's username
            
        Returns:
            Public store data
            
        Raises:
            NotFoundError: If store not found
        """
        store = await self.store_repo.get_by_username(username.lower())
        if not store:
            raise NotFoundError(message="Store not found", resource_type="Store")
        
        if not store.is_active:
            raise NotFoundError(message="Store not found", resource_type="Store")
        
        return self._store_to_dict(store)
    
    async def get_user_stores(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all stores owned by a user with stats.
        
        Args:
            user_id: Owner's user ID
            
        Returns:
            List of store summaries with stats
        """
        return await self.store_repo.get_with_stats(user_id)
    
    async def update_store(
        self,
        store_id: str,
        user_id: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Update store details.
        
        Args:
            store_id: Store's unique identifier
            user_id: Requesting user's ID
            **kwargs: Fields to update
            
        Returns:
            Updated store data
            
        Raises:
            NotFoundError: If store not found
            AuthorizationError: If user doesn't own the store
        """
        store = await self.store_repo.get_by_id(store_id)
        if not store:
            raise NotFoundError(message="Store not found", resource_type="Store")
        
        if store.user_id != user_id:
            raise AuthorizationError(message="You don't have access to this store")
        
        # Map field names
        field_mapping = {
            "name": "display_name",
            "logo": "logo_url",
            "banner": "banner_url",
        }
        
        updates = {}
        for key, value in kwargs.items():
            if value is not None:
                field = field_mapping.get(key, key)
                updates[field] = value
        
        if updates:
            store = await self.store_repo.update(store_id, **updates)
        
        logger.info(f"Store updated: {store_id}")
        return self._store_to_dict(store)
    
    async def toggle_store_status(
        self,
        store_id: str,
        user_id: str,
        is_active: bool,
    ) -> Dict[str, Any]:
        """
        Activate or deactivate a store.
        
        Args:
            store_id: Store's unique identifier
            user_id: Requesting user's ID
            is_active: New status
            
        Returns:
            Updated store data
        """
        store = await self.store_repo.get_by_id(store_id)
        if not store:
            raise NotFoundError(message="Store not found", resource_type="Store")
        
        if store.user_id != user_id:
            raise AuthorizationError(message="You don't have access to this store")
        
        store = await self.store_repo.update(store_id, is_active=is_active)
        
        status = "activated" if is_active else "deactivated"
        logger.info(f"Store {status}: {store_id}")
        return self._store_to_dict(store)
    
    async def delete_store(self, store_id: str, user_id: str) -> None:
        """
        Delete a store (soft delete).
        
        Args:
            store_id: Store's unique identifier
            user_id: Requesting user's ID
            
        Raises:
            NotFoundError: If store not found
            AuthorizationError: If user doesn't own the store
        """
        store = await self.store_repo.get_by_id(store_id)
        if not store:
            raise NotFoundError(message="Store not found", resource_type="Store")
        
        if store.user_id != user_id:
            raise AuthorizationError(message="You don't have access to this store")
        
        await self.store_repo.delete(store_id)
        logger.info(f"Store deleted: {store_id}")
    
    async def check_username_availability(self, username: str) -> Dict[str, Any]:
        """
        Check if a username is available.
        
        Args:
            username: Username to check
            
        Returns:
            Availability status and suggestions
        """
        username_lower = username.lower()
        available = not await self.store_repo.username_exists(username_lower)
        
        result = {
            "username": username_lower,
            "available": available,
        }
        
        if not available:
            result["suggestions"] = await self.store_repo.generate_username_suggestions(
                username_lower
            )
        
        return result
    
    def _store_to_dict(self, store) -> Dict[str, Any]:
        """Convert store model to dictionary."""
        return {
            "id": store.id,
            "user_id": store.user_id,
            "username": store.username,
            "display_name": store.display_name,
            "description": store.description,
            "logo_url": store.logo_url,
            "banner_url": store.banner_url,
            "template_id": store.template_id,
            "category": store.category,
            "custom_colors": store.custom_colors,
            "custom_fonts": store.custom_fonts,
            "social_links": store.social_links,
            "is_active": store.is_active,
            "created_at": str(store.created_at),
            "updated_at": str(store.updated_at) if store.updated_at else None,
        }
