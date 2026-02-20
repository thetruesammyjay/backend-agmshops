"""
AGM Store Builder - Order Schemas

Pydantic schemas for order-related requests and responses.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import PaginationMeta


class OrderItem(BaseModel):
    """Order item in create request."""
    product_id: str
    quantity: int = Field(ge=1)
    variant_selection: Optional[Dict[str, str]] = None


class CreateOrderRequest(BaseModel):
    """Create order request (public checkout)."""
    store_username: str
    customer_name: str = Field(min_length=2, max_length=255)
    customer_email: Optional[EmailStr] = None
    customer_phone: str
    delivery_address: str
    delivery_state: str
    delivery_lga: Optional[str] = None
    items: List[OrderItem]
    notes: Optional[str] = None
    discount: float = 0
    shipping_fee: float = 0


class UpdateOrderStatusRequest(BaseModel):
    """Update order status request."""
    status: str = Field(pattern="^(pending|confirmed|processing|shipped|delivered|cancelled)$")


class OrderItemData(BaseModel):
    """Order item in response."""
    id: Optional[str] = None
    product_id: str
    product_name: str
    product_image: Optional[str] = None
    product_price: float
    quantity: int
    subtotal: float
    variant_selection: Optional[Dict[str, str]] = None


class PaymentAccountDetails(BaseModel):
    """Payment virtual account details."""
    accountNumber: str
    accountName: str
    bankName: str
    amount: float


class PaymentData(BaseModel):
    """Payment data in order response."""
    id: str
    payment_reference: str
    amount: float
    status: str
    accountDetails: Optional[PaymentAccountDetails] = None
    paid_at: Optional[str] = None
    expires_at: Optional[str] = None
    created_at: str


class OrderData(BaseModel):
    """Order data."""
    id: str
    order_number: str
    store_id: str
    store_name: Optional[str] = None
    customer_name: str
    customer_email: Optional[str] = None
    customer_phone: str
    delivery_address: str
    delivery_state: str
    delivery_lga: Optional[str] = None
    subtotal: float
    discount: float = 0
    shipping_fee: float = 0
    agm_fee: float = 0
    total: float
    status: str = "pending"
    payment_status: str = "pending"
    notes: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None


class OrderDetailData(OrderData):
    """Order detail with items and payment."""
    items: List[OrderItemData] = []
    payment: Optional[PaymentData] = None


class OrderSummary(BaseModel):
    """Order summary for lists."""
    id: str
    order_number: str
    store_id: str
    store_name: Optional[str] = None
    customer_name: str
    customer_email: Optional[str] = None
    customer_phone: str
    total: float
    status: str
    payment_status: str
    created_at: str


class TrackingEvent(BaseModel):
    """Order tracking event."""
    status: str
    timestamp: str


class OrderTrackingData(BaseModel):
    """Order tracking data."""
    order_number: str
    status: str
    payment_status: str
    customer_name: str
    total: float
    created_at: str
    items: List[OrderItemData]
    tracking_history: List[TrackingEvent] = []


class CreateOrderResponseData(BaseModel):
    """Create order response data."""
    order: OrderData
    items: List[OrderItemData]
    payment: PaymentData


class OrderResponse(BaseModel):
    """Order response."""
    success: bool = True
    data: OrderData


class OrderDetailResponse(BaseModel):
    """Order detail response."""
    success: bool = True
    data: CreateOrderResponseData
    message: Optional[str] = None


class OrderListResponse(BaseModel):
    """Order list response."""
    success: bool = True
    data: List[OrderSummary]
    pagination: PaginationMeta


class OrderTrackingResponse(BaseModel):
    """Order tracking response."""
    success: bool = True
    data: OrderTrackingData
