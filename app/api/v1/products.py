"""
AGM Store Builder - Product Endpoints

Product management endpoints for creating, updating, and listing products.
"""

from typing import Optional, List
from fastapi import APIRouter, status, Query

from app.api.deps import DatabaseSession, CurrentUserId, OptionalUserId
from app.services.product_service import ProductService
from app.schemas.product import (
    CreateProductRequest,
    UpdateProductRequest,
    ProductResponse,
    ProductListResponse,
    ProductDetailResponse,
    UpdateStockRequest,
    ToggleProductStatusRequest,
    BulkUpdateRequest,
)
from app.schemas.common import MessageResponse, PaginationParams

router = APIRouter()


@router.post(
    "",
    response_model=ProductDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    request: CreateProductRequest,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Create a new product.
    
    Creates a product for the specified store.
    """
    product_service = ProductService(db)
    product = await product_service.create_product(
        user_id=user_id,
        **request.model_dump(),
    )
    
    return {
        "success": True,
        "data": product,
        "message": "Product created successfully",
    }


@router.get("/my-products", response_model=ProductListResponse)
async def get_my_products(
    user_id: CurrentUserId,
    db: DatabaseSession,
    store_id: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
):
    """
    Get all products for the authenticated user's stores.
    
    Supports filtering by store, category, and search.
    """
    product_service = ProductService(db)
    result = await product_service.get_user_products(
        user_id=user_id,
        store_id=store_id,
        page=page,
        limit=limit,
        search=search,
        category=category,
        product_status=status,
    )
    
    return {
        "success": True,
        "data": result["products"],
        "pagination": result["pagination"],
    }


@router.get("/{product_id}", response_model=ProductDetailResponse)
async def get_product_by_id(
    product_id: str,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Get product details by ID (owner only).
    
    Returns full product details for the owner.
    """
    product_service = ProductService(db)
    product = await product_service.get_product_by_id(product_id, user_id)
    
    return {
        "success": True,
        "data": product,
    }


@router.put("/{product_id}", response_model=ProductDetailResponse)
async def update_product(
    product_id: str,
    request: UpdateProductRequest,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Update product details (owner only).
    
    Updates product information.
    """
    product_service = ProductService(db)
    product = await product_service.update_product(
        product_id=product_id,
        user_id=user_id,
        **request.model_dump(exclude_unset=True),
    )
    
    return {
        "success": True,
        "data": product,
        "message": "Product updated successfully",
    }


@router.patch("/{product_id}/stock", response_model=ProductDetailResponse)
async def update_stock(
    product_id: str,
    request: UpdateStockRequest,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Update product stock quantity.
    
    Supports set, increment, and decrement operations.
    """
    product_service = ProductService(db)
    product = await product_service.update_stock(
        product_id=product_id,
        user_id=user_id,
        stock_quantity=request.stock_quantity,
        operation=request.operation,
        quantity=request.quantity,
    )
    
    return {
        "success": True,
        "data": product,
        "message": "Stock updated successfully",
    }


@router.patch("/{product_id}/status", response_model=ProductDetailResponse)
async def toggle_product_status(
    product_id: str,
    request: ToggleProductStatusRequest,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Activate or deactivate a product.
    
    Toggles the product's active status.
    """
    product_service = ProductService(db)
    product = await product_service.toggle_product_status(
        product_id=product_id,
        user_id=user_id,
        is_active=request.is_active,
    )
    
    status_text = "activated" if request.is_active else "deactivated"
    
    return {
        "success": True,
        "data": product,
        "message": f"Product {status_text} successfully",
    }


@router.delete("/{product_id}", response_model=MessageResponse)
async def delete_product(
    product_id: str,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Delete a product (soft delete).
    
    Marks the product as deleted but preserves data.
    """
    product_service = ProductService(db)
    await product_service.delete_product(product_id, user_id)
    
    return {
        "success": True,
        "message": "Product deleted successfully",
    }


@router.patch("/bulk-update", response_model=MessageResponse)
async def bulk_update_products(
    request: BulkUpdateRequest,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Update multiple products at once.
    
    Applies the same updates to all specified products.
    """
    product_service = ProductService(db)
    count = await product_service.bulk_update(
        product_ids=request.product_ids,
        user_id=user_id,
        updates=request.updates,
    )
    
    return {
        "success": True,
        "data": {"updated_count": count},
        "message": "Products updated successfully",
    }
