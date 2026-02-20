"""
AGM Store Builder - Store Repository

Data access layer for store operations.
"""

from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store import Store
from app.models.product import Product
from app.models.order import Order
from app.repositories.base import BaseRepository


class StoreRepository(BaseRepository[Store]):
    """Repository for store data operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, Store)
    
    async def get_by_username(self, username: str) -> Optional[Store]:
        """Get store by username."""
        result = await self.db.execute(
            select(Store).where(
                Store.username == username,
                Store.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: str) -> List[Store]:
        """Get all stores owned by a user."""
        result = await self.db.execute(
            select(Store).where(
                Store.user_id == user_id,
                Store.deleted_at.is_(None),
            ).order_by(Store.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def username_exists(self, username: str, exclude_id: Optional[str] = None) -> bool:
        """Check if username already exists."""
        query = select(Store.id).where(
            Store.username == username,
            Store.deleted_at.is_(None),
        )
        if exclude_id:
            query = query.where(Store.id != exclude_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
    
    async def get_with_stats(self, user_id: str) -> List[dict]:
        """Get user's stores with product and order counts."""
        stores = await self.get_by_user_id(user_id)
        result = []
        
        for store in stores:
            # Get product count
            product_count_result = await self.db.execute(
                select(func.count(Product.id)).where(
                    Product.store_id == store.id,
                    Product.deleted_at.is_(None),
                )
            )
            product_count = product_count_result.scalar() or 0
            
            # Get order count and revenue
            order_result = await self.db.execute(
                select(
                    func.count(Order.id),
                    func.coalesce(func.sum(Order.total), 0),
                ).where(
                    Order.store_id == store.id,
                    Order.deleted_at.is_(None),
                    Order.payment_status == 'paid',
                )
            )
            row = order_result.one()
            order_count = row[0] or 0
            total_revenue = float(row[1] or 0)
            
            result.append({
                "id": store.id,
                "name": store.display_name,
                "username": store.username,
                "logo": store.logo_url,
                "is_active": store.is_active,
                "product_count": product_count,
                "order_count": order_count,
                "total_revenue": total_revenue,
                "created_at": str(store.created_at),
            })
        
        return result
    
    async def generate_username_suggestions(self, base_username: str, count: int = 3) -> List[str]:
        """Generate available username suggestions."""
        suggestions: List[str] = []
        suffix = 1
        
        while len(suggestions) < count:
            candidate = f"{base_username}{suffix}"
            if not await self.username_exists(candidate):
                suggestions.append(candidate)
            suffix += 1
            
            # Safety limit
            if suffix > 100:
                break
        
        return suggestions
