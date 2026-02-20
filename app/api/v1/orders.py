"""
AGM Store Builder - Order Endpoints

Order management endpoints for creating, tracking, and managing orders.
"""

from typing import Optional
from fastapi import APIRouter, status, Query

from app.api.deps import DatabaseSession, CurrentUserId
from app.services.order_service import OrderService
from app.schemas.order import (
    CreateOrderRequest,
    OrderResponse,
    OrderListResponse,
    OrderDetailResponse,
    OrderTrackingResponse,
    UpdateOrderStatusRequest,
)
from app.schemas.common import MessageResponse

router = APIRouter()


@router.post(
    "",
    response_model=OrderDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    request: CreateOrderRequest,
    db: DatabaseSession,
):
    """
    Create a new order (public checkout).
    
    Creates an order with payment details.
    This is a public endpoint for customer checkout.
    """
    order_service = OrderService(db)
    result = await order_service.create_order(
        store_username=request.store_username,
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


@router.get("/track/{order_number}", response_model=OrderTrackingResponse)
async def track_order(
    order_number: str,
    db: DatabaseSession,
):
    """
    Track an order by order number (public).
    
    Returns order status and tracking history.
    """
    order_service = OrderService(db)
    result = await order_service.track_order(order_number)
    
    return {
        "success": True,
        "data": result,
    }


@router.get("", response_model=OrderListResponse)
async def list_orders(
    user_id: CurrentUserId,
    db: DatabaseSession,
    store_id: Optional[str] = None,
    status: Optional[str] = None,
    payment_status: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
):
    """
    Get all orders for the user's stores.
    
    Supports filtering by store, status, and date range.
    """
    order_service = OrderService(db)
    result = await order_service.get_user_orders(
        user_id=user_id,
        store_id=store_id,
        status=status,
        payment_status=payment_status,
        page=page,
        limit=limit,
        search=search,
        date_from=date_from,
        date_to=date_to,
    )
    
    return {
        "success": True,
        "data": result["orders"],
        "pagination": result["pagination"],
    }


@router.get("/{order_id}", response_model=OrderDetailResponse)
async def get_order(
    order_id: str,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Get order details by ID (owner only).
    
    Returns full order details including items and payment.
    """
    order_service = OrderService(db)
    order = await order_service.get_order_details(order_id, user_id)
    
    return {
        "success": True,
        "data": order,
    }


@router.patch("/{order_id}/status", response_model=OrderDetailResponse)
async def update_order_status(
    order_id: str,
    request: UpdateOrderStatusRequest,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Update order status (owner only).
    
    Updates the order status with proper validation.
    """
    order_service = OrderService(db)
    order = await order_service.update_order_status(
        order_id=order_id,
        user_id=user_id,
        new_status=request.status,
    )
    
    return {
        "success": True,
        "data": order,
        "message": "Order status updated successfully",
    }


@router.delete("/{order_id}", response_model=MessageResponse)
async def cancel_order(
    order_id: str,
    user_id: CurrentUserId,
    db: DatabaseSession,
):
    """
    Cancel an order (owner only).
    
    Only works for pending or confirmed orders.
    """
    order_service = OrderService(db)
    await order_service.cancel_order(order_id, user_id)
    
    return {
        "success": True,
        "message": "Order cancelled successfully",
    }
