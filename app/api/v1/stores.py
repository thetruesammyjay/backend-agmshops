"""
AGM Store Builder - Store Endpoints

Store management endpoints for creating, updating, and managing stores.
"""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter, status, Query

from app.api.deps import DatabaseSession, CurrentUserId, OptionalUserId
from app.services.store_service import StoreService
from app.schemas.store import (
    CreateStoreRequest,
    UpdateStoreRequest,
    StoreResponse,
    StoreListResponse,
    StoreDetailResponse,
    CheckUsernameResponse,
    ToggleStatusRequest,
)
from app.schemas.common import MessageResponse
from app.schemas.order import OrderItem

router = APIRouter()


class CheckoutRequest(BaseModel):
    """Public checkout request via store route."""
    customer_name: str = Field(min_length=2, max_length=255)
    customer_email: Optional[EmailStr] = None
    customer_phone: str
    delivery_address: str = ""
    delivery_state: str = ""
    delivery_lga: Optional[str] = None
    items: List[OrderItem]
    notes: Optional[str] = None
    discount: float = 0
    shipping_fee: float = 0


@router.post(
    "",
    response_model=StoreDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_store(
    request: CreateStoreRequest,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Create a new store.
    
    Creates a store for the authenticated user.
    """
    store_service = StoreService(db)
    store = await store_service.create_store(
        user_id=user_id,
        name=request.name,
        username=request.username,
        description=request.description,
        category=request.category,
        logo=request.logo,
        banner=request.banner,
        social_links=request.social_links,
    )
    
    return {
        "success": True,
        "data": store,
        "message": "Store created successfully",
    }


@router.get("/check/{username}", response_model=CheckUsernameResponse)
async def check_username(
    username: str,
    db: DatabaseSession,
):
    """
    Check if a store username is available.
    
    Returns availability status and suggestions if taken.
    """
    store_service = StoreService(db)
    result = await store_service.check_username_availability(username)
    
    return {
        "success": True,
        "data": result,
    }


@router.get("/my-stores", response_model=StoreListResponse)
async def get_my_stores(
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Get all stores owned by the authenticated user.
    
    Returns a list of stores with summary statistics.
    """
    store_service = StoreService(db)
    stores = await store_service.get_user_stores(user_id)
    
    return {
        "success": True,
        "data": stores,
    }


@router.get("/{username}/products")
async def get_store_products(
    username: str,
    db: DatabaseSession,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    sortBy: Optional[str] = None,
):
    """
    Get public products for a store by username.
    
    Returns paginated list of active products for the store.
    """
    from app.services.product_service import ProductService
    
    store_service = StoreService(db)
    store = await store_service.get_store_by_username(username)
    
    product_service = ProductService(db)
    result = await product_service.get_store_products(
        store_id=store["id"],
        page=page,
        limit=limit,
        search=search,
        category=category,
        sort_by=sortBy,
    )
    
    return {
        "success": True,
        "data": result["products"],
        "pagination": result["pagination"],
    }


@router.get("/{username}/products/{product_id}")
async def get_store_product(
    username: str,
    product_id: str,
    db: DatabaseSession,
):
    """
    Get a specific product from a store by username.
    
    Returns product details for the specified product.
    """
    from app.services.product_service import ProductService
    
    store_service = StoreService(db)
    store = await store_service.get_store_by_username(username)
    
    product_service = ProductService(db)
    product = await product_service.get_public_product(
        store_id=store["id"],
        product_id=product_id,
    )
    
    return {
        "success": True,
        "data": product,
    }


@router.get("/{username}", response_model=StoreDetailResponse)
async def get_store_by_username(
    username: str,
    db: DatabaseSession,
):
    """
    Get public store details by username.
    
    Returns store information visible to the public.
    """
    store_service = StoreService(db)
    store = await store_service.get_store_by_username(username)
    
    return {
        "success": True,
        "data": store,
    }


@router.get("/id/{store_id}", response_model=StoreDetailResponse)
async def get_store_by_id(
    store_id: str,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Get store details by ID (owner only).
    
    Returns full store details for the owner.
    """
    store_service = StoreService(db)
    store = await store_service.get_store_by_id(store_id, user_id)
    
    return {
        "success": True,
        "data": store,
    }


@router.put("/{store_id}", response_model=StoreDetailResponse)
async def update_store(
    store_id: str,
    request: UpdateStoreRequest,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Update store details (owner only).
    
    Updates store information for the authenticated owner.
    """
    store_service = StoreService(db)
    store = await store_service.update_store(
        store_id=store_id,
        user_id=user_id,
        **request.model_dump(exclude_unset=True),
    )
    
    return {
        "success": True,
        "data": store,
        "message": "Store updated successfully",
    }


@router.patch("/{store_id}/status", response_model=StoreDetailResponse)
async def toggle_store_status(
    store_id: str,
    request: ToggleStatusRequest,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Activate or deactivate a store.
    
    Toggles the store's active status.
    """
    store_service = StoreService(db)
    store = await store_service.toggle_store_status(
        store_id=store_id,
        user_id=user_id,
        is_active=request.is_active,
    )
    
    status_text = "activated" if request.is_active else "deactivated"
    
    return {
        "success": True,
        "data": store,
        "message": f"Store {status_text} successfully",
    }


@router.delete("/{store_id}", response_model=MessageResponse)
async def delete_store(
    store_id: str,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Delete a store (soft delete).
    
    Marks the store as deleted but preserves data.
    """
    store_service = StoreService(db)
    await store_service.delete_store(store_id, user_id)
    
    return {
        "success": True,
        "message": "Store deleted successfully",
    }


@router.post("/{store_id}/checkout", status_code=status.HTTP_201_CREATED)
async def store_checkout(
    store_id: str,
    request: CheckoutRequest,
    db: DatabaseSession,
):
    """
    Create an order via store checkout (public).

    Resolves the store by ID and creates an order with payment details.
    """
    from app.services.order_service import OrderService

    # Look up store by ID (try both ID and username for flexibility)
    store_service = StoreService(db)
    try:
        store = await store_service.get_store_by_username(store_id)
    except Exception:
        # If not found by username, try repo get_by_id directly
        store_obj = await store_service.store_repo.get_by_id(store_id)
        if not store_obj or not store_obj.is_active:
            from app.core.exceptions import NotFoundError
            raise NotFoundError(message="Store not found", resource_type="Store")
        store = store_service._store_to_dict(store_obj)

    order_service = OrderService(db)
    result = await order_service.create_order(
        store_username=store["username"],
        customer_name=request.customer_name,
        customer_email=request.customer_email,
        customer_phone=request.customer_phone,
        delivery_address=request.delivery_address,
        delivery_state=request.delivery_state,
        delivery_lga=request.delivery_lga,
        items=[item.model_dump() for item in request.items],
        notes=request.notes,
        discount=request.discount,
        shipping_fee=request.shipping_fee,
    )

    return {
        "success": True,
        "data": result,
        "message": "Order created successfully. Please complete payment.",
    }

