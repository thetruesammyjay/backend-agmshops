"""
AGM Store Builder - Product Repository

Data access layer for product operations.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, update, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.models.store import Store
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """Repository for product data operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, Product)
    
    async def get_by_store(
        self,
        store_id: str,
        page: int = 1,
        limit: int = 20,
        category: Optional[str] = None,
        search: Optional[str] = None,
        sort: str = "newest",
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        in_stock: Optional[bool] = None,
        featured: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Get products by store with filters and pagination."""
        query = select(Product).where(
            Product.store_id == store_id,
            Product.deleted_at.is_(None),
            Product.is_active == True,
        )
        
        # Apply filters
        if category:
            query = query.where(Product.category == category)
        
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term),
                )
            )
        
        if min_price is not None:
            query = query.where(Product.price >= min_price)
        
        if max_price is not None:
            query = query.where(Product.price <= max_price)
        
        if in_stock is not None:
            if in_stock:
                query = query.where(Product.stock_quantity > 0)
            else:
                query = query.where(Product.stock_quantity == 0)
        
        if featured is not None:
            query = query.where(Product.is_featured == featured)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0
        
        # Apply sorting
        if sort == "price_asc":
            query = query.order_by(Product.price.asc())
        elif sort == "price_desc":
            query = query.order_by(Product.price.desc())
        elif sort == "name_asc":
            query = query.order_by(Product.name.asc())
        elif sort == "name_desc":
            query = query.order_by(Product.name.desc())
        elif sort == "popular":
            query = query.order_by(Product.view_count.desc())
        else:  # newest
            query = query.order_by(Product.created_at.desc())
        
        # Apply pagination
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)
        
        result = await self.db.execute(query)
        products = list(result.scalars().all())
        
        return {
            "products": products,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit,
                "hasMore": offset + len(products) < total,
            },
        }
    
    async def get_user_products(
        self,
        user_id: str,
        store_id: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        category: Optional[str] = None,
        product_status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get all products for a user's stores."""
        # Build base query with store join
        query = (
            select(Product, Store.display_name.label("store_name"))
            .join(Store, Product.store_id == Store.id)
            .where(
                Store.user_id == user_id,
                Product.deleted_at.is_(None),
                Store.deleted_at.is_(None),
            )
        )
        
        if store_id:
            query = query.where(Product.store_id == store_id)
        
        if search:
            search_term = f"%{search}%"
            query = query.where(Product.name.ilike(search_term))
        
        if category:
            query = query.where(Product.category == category)
        
        if product_status == "active":
            query = query.where(Product.is_active == True)
        elif product_status == "inactive":
            query = query.where(Product.is_active == False)
        elif product_status == "out_of_stock":
            query = query.where(Product.stock_quantity == 0)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0
        
        # Apply pagination
        offset = (page - 1) * limit
        query = query.order_by(Product.created_at.desc()).offset(offset).limit(limit)
        
        result = await self.db.execute(query)
        rows = result.all()
        
        products = []
        for row in rows:
            product = row[0]
            store_name = row[1]
            products.append({
                "id": product.id,
                "store_id": product.store_id,
                "store_name": store_name,
                "name": product.name,
                "price": float(product.price),
                "stock_quantity": product.stock_quantity,
                "images": product.images or [],
                "is_active": product.is_active,
                "created_at": str(product.created_at),
            })
        
        return {
            "products": products,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit,
                "hasMore": offset + len(products) < total,
            },
        }
    
    async def get_store_products(
        self,
        store_id: str,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        category: Optional[str] = None,
        sort_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get public products for a store (wrapper for get_by_store)."""
        # Map sort_by to sort parameter
        sort_mapping = {
            "createdAt": "newest",
            "price": "price_asc",
            "priceDesc": "price_desc",
            "name": "name_asc",
            "popular": "popular",
        }
        sort = sort_mapping.get(sort_by, "newest") if sort_by else "newest"
        
        result = await self.get_by_store(
            store_id=store_id,
            page=page,
            limit=limit,
            search=search,
            category=category,
            sort=sort,
        )
        
        # Convert products to dicts for JSON serialization
        products = []
        for product in result["products"]:
            products.append({
                "id": product.id,
                "store_id": product.store_id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "compare_price": float(product.compare_at_price) if product.compare_at_price else None,
                "stock_quantity": product.stock_quantity,
                "images": product.images or [],
                "category": product.category,
                "is_active": product.is_active,
                "is_featured": product.is_featured,
                "created_at": str(product.created_at),
            })
        
        return {
            "products": products,
            "pagination": result["pagination"],
        }
    
    async def update_stock(
        self,
        product_id: str,
        quantity: int,
        operation: str = "set",
    ) -> Optional[Product]:
        """Update product stock quantity."""
        product = await self.get_by_id(product_id)
        if not product:
            return None
        
        if operation == "set":
            new_quantity = quantity
        elif operation == "increment":
            new_quantity = product.stock_quantity + quantity
        elif operation == "decrement":
            new_quantity = max(0, product.stock_quantity - quantity)
        else:
            new_quantity = quantity
        
        await self.db.execute(
            update(Product)
            .where(Product.id == product_id)
            .values(stock_quantity=new_quantity)
        )
        await self.db.commit()
        
        return await self.get_by_id(product_id)
    
    async def increment_view_count(self, product_id: str) -> None:
        """Increment product view count."""
        await self.db.execute(
            update(Product)
            .where(Product.id == product_id)
            .values(view_count=Product.view_count + 1)
        )
        await self.db.commit()
    
    async def bulk_update(
        self,
        product_ids: List[str],
        user_id: str,
        updates: Dict[str, Any],
    ) -> int:
        """Bulk update multiple products."""
        # Verify ownership through stores
        query = (
            select(Product.id)
            .join(Store, Product.store_id == Store.id)
            .where(
                Product.id.in_(product_ids),
                Store.user_id == user_id,
                Product.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(query)
        valid_ids = [row[0] for row in result.all()]
        
        if not valid_ids:
            return 0
        
        await self.db.execute(
            update(Product)
            .where(Product.id.in_(valid_ids))
            .values(**updates)
        )
        await self.db.commit()
        
        return len(valid_ids)
