"""
AGM Store Builder - Base Repository

Base repository class with common CRUD operations.
"""

from typing import Generic, TypeVar, Optional, List, Type, Any
from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """
    Base repository with common CRUD operations.
    
    Provides generic database operations that can be inherited
    by specific entity repositories.
    """
    
    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model
    
    def generate_id(self) -> str:
        """Generate a new UUID string."""
        return str(uuid4())
    
    async def create(self, **kwargs: Any) -> T:
        """
        Create a new entity.
        
        Args:
            **kwargs: Entity field values
            
        Returns:
            Created entity
        """
        if 'id' not in kwargs:
            kwargs['id'] = self.generate_id()
        
        entity = self.model(**kwargs)
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
    
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Get entity by ID.
        
        Args:
            entity_id: Entity's unique identifier
            
        Returns:
            Entity or None if not found
        """
        query = select(self.model).where(self.model.id == entity_id)  # type: ignore
        
        # Check for soft delete
        if hasattr(self.model, 'deleted_at'):
            query = query.where(self.model.deleted_at.is_(None))  # type: ignore
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[T]:
        """
        Get all entities with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records
            
        Returns:
            List of entities
        """
        query = select(self.model)
        
        if hasattr(self.model, 'deleted_at'):
            query = query.where(self.model.deleted_at.is_(None))  # type: ignore
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def update(self, entity_id: str, **kwargs: Any) -> Optional[T]:
        """
        Update an entity by ID.
        
        Args:
            entity_id: Entity's unique identifier
            **kwargs: Fields to update
            
        Returns:
            Updated entity or None
        """
        await self.db.execute(
            update(self.model)
            .where(self.model.id == entity_id)  # type: ignore
            .values(**kwargs)
        )
        await self.db.commit()
        return await self.get_by_id(entity_id)
    
    async def delete(self, entity_id: str) -> bool:
        """
        Delete an entity (soft delete if supported).
        
        Args:
            entity_id: Entity's unique identifier
            
        Returns:
            True if deleted
        """
        entity = await self.get_by_id(entity_id)
        if not entity:
            return False
        
        if hasattr(entity, 'soft_delete'):
            entity.soft_delete()
            await self.db.commit()
        else:
            await self.db.delete(entity)
            await self.db.commit()
        
        return True
    
    async def count(self) -> int:
        """
        Count total entities.
        
        Returns:
            Total count
        """
        query = select(func.count(self.model.id))  # type: ignore
        
        if hasattr(self.model, 'deleted_at'):
            query = query.where(self.model.deleted_at.is_(None))  # type: ignore
        
        result = await self.db.execute(query)
        return result.scalar() or 0
