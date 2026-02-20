"""
AGM Store Builder - User Repository

Data access layer for user operations.
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """Repository for user data operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(
        self,
        email: str,
        password_hash: str,
        full_name: str,
        phone: Optional[str] = None,
    ) -> User:
        """Create a new user."""
        user = User(
            id=str(uuid4()),
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            phone=phone,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id, User.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email, User.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()
    
    async def get_by_phone(self, phone: str) -> Optional[User]:
        """Get user by phone number."""
        result = await self.db.execute(
            select(User).where(User.phone == phone, User.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()
    
    async def update_last_login(self, user_id: str) -> None:
        """Update user's last login time."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(last_login_at=datetime.now(timezone.utc))
        )
        await self.db.commit()
    
    async def mark_email_verified(self, user_id: str) -> None:
        """Mark user's email as verified."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(email_verified=True)
        )
        await self.db.commit()
    
    async def update_password(self, user_id: str, password_hash: str) -> None:
        """Update user's password."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(password_hash=password_hash)
        )
        await self.db.commit()
    
    async def update(self, user_id: str, **kwargs) -> Optional[User]:
        """Update user fields."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(**kwargs)
        )
        await self.db.commit()
        return await self.get_by_id(user_id)
    
    async def soft_delete(self, user_id: str) -> None:
        """Soft delete a user."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                deleted_at=datetime.now(timezone.utc),
                is_active=False,
            )
        )
        await self.db.commit()
