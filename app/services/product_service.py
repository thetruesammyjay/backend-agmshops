"""
AGM Store Builder - Product Service

Business logic for product management.
"""

from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.core.exceptions import NotFoundError, AuthorizationError
from app.repositories.product_repository import ProductRepository
from app.repositories.store_repository import StoreRepository


class ProductService:
    """Product service for product management operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.product_repo = ProductRepository(db)
        self.store_repo = StoreRepository(db)
    
    async def create_product(
        self,
        user_id: str,
        store_id: str,
        name: str,
        price: float,
        description: Optional[str] = None,
        compare_price: Optional[float] = None,
        cost_price: Optional[float] = None,
        sku: Optional[str] = None,
        barcode: Optional[str] = None,
        stock_quantity: int = 0,
        low_stock_threshold: int = 5,
        weight: Optional[float] = None,
        dimensions: Optional[Dict[str, Any]] = None,
        images: Optional[List[str]] = None,
        variants: Optional[List[Dict[str, Any]]] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        is_featured: bool = False,
    ) -> Dict[str, Any]:
        """Create a new product."""
        # Verify store ownership
        store = await self.store_repo.get_by_id(store_id)
        if not store:
            raise NotFoundError(message="Store not found", resource_type="Store")
        
        if store.user_id != user_id:
            raise AuthorizationError(message="You don't have access to this store")
        
        product = await self.product_repo.create(
            store_id=store_id,
            name=name,
            description=description,
            price=price,
            compare_at_price=compare_price,
            cost_price=cost_price,
            sku=sku,
            barcode=barcode,
            stock_quantity=stock_quantity,
            low_stock_threshold=low_stock_threshold,
            weight=weight,
            dimensions=dimensions,
            images=images or [],
            variations=variants,
            category=category,
            tags=tags,
            is_featured=is_featured,
        )
        
        logger.info(f"Product created: {product.id} in store {store_id}")
        return self._product_to_dict(product)
    
    async def get_product_by_id(self, product_id: str, user_id: str) -> Dict[str, Any]:
        """Get product by ID (owner only)."""
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError(message="Product not found", resource_type="Product")
        
        # Verify ownership through store
        store = await self.store_repo.get_by_id(product.store_id)
        if not store or store.user_id != user_id:
            raise AuthorizationError(message="You don't have access to this product")
        
        return self._product_to_dict(product)
    
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
        return await self.product_repo.get_user_products(
            user_id=user_id,
            store_id=store_id,
            page=page,
            limit=limit,
            search=search,
            category=category,
            product_status=product_status,
        )
    
    async def get_store_products(
        self,
        store_id: str,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        category: Optional[str] = None,
        sort_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get public products for a store (for storefront)."""
        return await self.product_repo.get_store_products(
            store_id=store_id,
            page=page,
            limit=limit,
            search=search,
            category=category,
            sort_by=sort_by,
        )
    
    async def get_public_product(
        self,
        store_id: str,
        product_id: str,
    ) -> Dict[str, Any]:
        """Get a single product by ID for public storefront."""
        product = await self.product_repo.get_by_id(product_id)
        if not product or product.store_id != store_id:
            raise NotFoundError(message="Product not found", resource_type="Product")
        
        if not product.is_active:
            raise NotFoundError(message="Product not found", resource_type="Product")
        
        # Increment view count
        await self.product_repo.increment_view_count(product_id)
        
        return self._product_to_dict(product)
    
    async def update_product(
        self,
        product_id: str,
        user_id: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """Update product details."""
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError(message="Product not found", resource_type="Product")
        
        # Verify ownership
        store = await self.store_repo.get_by_id(product.store_id)
        if not store or store.user_id != user_id:
            raise AuthorizationError(message="You don't have access to this product")
        
        # Map field names
        field_mapping = {
            "compare_price": "compare_at_price",
            "variants": "variations",
        }
        
        updates = {}
        for key, value in kwargs.items():
            if value is not None:
                field = field_mapping.get(key, key)
                updates[field] = value
        
        if updates:
            product = await self.product_repo.update(product_id, **updates)
        
        logger.info(f"Product updated: {product_id}")
        return self._product_to_dict(product)
    
    async def update_stock(
        self,
        product_id: str,
        user_id: str,
        stock_quantity: Optional[int] = None,
        operation: str = "set",
        quantity: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update product stock quantity."""
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError(message="Product not found", resource_type="Product")
        
        # Verify ownership
        store = await self.store_repo.get_by_id(product.store_id)
        if not store or store.user_id != user_id:
            raise AuthorizationError(message="You don't have access to this product")
        
        qty = stock_quantity if stock_quantity is not None else quantity or 0
        product = await self.product_repo.update_stock(product_id, qty, operation)
        
        logger.info(f"Product stock updated: {product_id} ({operation}: {qty})")
        return self._product_to_dict(product)
    
    async def toggle_product_status(
        self,
        product_id: str,
        user_id: str,
        is_active: bool,
    ) -> Dict[str, Any]:
        """Activate or deactivate a product."""
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError(message="Product not found", resource_type="Product")
        
        # Verify ownership
        store = await self.store_repo.get_by_id(product.store_id)
        if not store or store.user_id != user_id:
            raise AuthorizationError(message="You don't have access to this product")
        
        product = await self.product_repo.update(product_id, is_active=is_active)
        
        status = "activated" if is_active else "deactivated"
        logger.info(f"Product {status}: {product_id}")
        return self._product_to_dict(product)
    
    async def delete_product(self, product_id: str, user_id: str) -> None:
        """Delete a product (soft delete)."""
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError(message="Product not found", resource_type="Product")
        
        # Verify ownership
        store = await self.store_repo.get_by_id(product.store_id)
        if not store or store.user_id != user_id:
            raise AuthorizationError(message="You don't have access to this product")
        
        await self.product_repo.delete(product_id)
        logger.info(f"Product deleted: {product_id}")
    
    async def bulk_update(
        self,
        product_ids: List[str],
        user_id: str,
        updates: Dict[str, Any],
    ) -> int:
        """Bulk update multiple products."""
        count = await self.product_repo.bulk_update(product_ids, user_id, updates)
        logger.info(f"Bulk updated {count} products for user {user_id}")
        return count
    
    def _product_to_dict(self, product) -> Dict[str, Any]:
        """Convert product model to dictionary."""
        return {
            "id": product.id,
            "store_id": product.store_id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "compare_price": float(product.compare_at_price) if product.compare_at_price else None,
            "cost_price": float(product.cost_price) if product.cost_price else None,
            "sku": product.sku,
            "barcode": product.barcode,
            "stock_quantity": product.stock_quantity,
            "low_stock_threshold": product.low_stock_threshold,
            "weight": float(product.weight) if product.weight else None,
            "dimensions": product.dimensions,
            "images": product.images or [],
            "variants": product.variations,
            "category": product.category,
            "tags": product.tags,
            "is_active": product.is_active,
            "is_featured": product.is_featured,
            "view_count": product.view_count,
            "created_at": str(product.created_at),
            "updated_at": str(product.updated_at) if product.updated_at else None,
        }
