"""
AGM Store Builder - Product Schemas

Pydantic schemas for product-related requests and responses.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

from app.schemas.common import PaginationMeta


class ProductVariant(BaseModel):
    """Product variant."""
    name: str
    options: List[str]


class ProductDimensions(BaseModel):
    """Product dimensions."""
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    unit: str = "cm"


class CreateProductRequest(BaseModel):
    """Create product request."""
    store_id: str
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(gt=0)
    compare_price: Optional[float] = None
    cost_price: Optional[float] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    stock_quantity: int = Field(default=0, ge=0)
    low_stock_threshold: int = Field(default=5, ge=0)
    weight: Optional[float] = None
    dimensions: Optional[Dict[str, Any]] = None
    images: List[str] = []
    variants: Optional[List[Dict[str, Any]]] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    is_featured: bool = False


class UpdateProductRequest(BaseModel):
    """Update product request."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    compare_price: Optional[float] = None
    cost_price: Optional[float] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    low_stock_threshold: Optional[int] = Field(None, ge=0)
    weight: Optional[float] = None
    dimensions: Optional[Dict[str, Any]] = None
    images: Optional[List[str]] = None
    variants: Optional[List[Dict[str, Any]]] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    is_featured: Optional[bool] = None


class UpdateStockRequest(BaseModel):
    """Update stock request."""
    stock_quantity: Optional[int] = None
    quantity: Optional[int] = None
    operation: str = Field(default="set", pattern="^(set|increment|decrement)$")


class ToggleProductStatusRequest(BaseModel):
    """Toggle product status request."""
    is_active: bool


class BulkUpdateRequest(BaseModel):
    """Bulk update products request."""
    product_ids: List[str]
    updates: Dict[str, Any]


class ProductData(BaseModel):
    """Product data."""
    id: str
    store_id: str
    name: str
    description: Optional[str] = None
    price: float
    compare_price: Optional[float] = None
    cost_price: Optional[float] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    stock_quantity: int = 0
    low_stock_threshold: int = 5
    weight: Optional[float] = None
    dimensions: Optional[Dict[str, Any]] = None
    images: List[str] = []
    variants: Optional[List[Dict[str, Any]]] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: bool = True
    is_featured: bool = False
    view_count: int = 0
    created_at: str
    updated_at: Optional[str] = None


class ProductSummary(BaseModel):
    """Product summary for lists."""
    id: str
    store_id: str
    store_name: Optional[str] = None
    name: str
    price: float
    stock_quantity: int = 0
    images: List[str] = []
    is_active: bool = True
    created_at: str


class ProductResponse(BaseModel):
    """Product response."""
    success: bool = True
    data: ProductData


class ProductDetailResponse(BaseModel):
    """Product detail response."""
    success: bool = True
    data: ProductData
    message: Optional[str] = None


class ProductListResponse(BaseModel):
    """Product list response."""
    success: bool = True
    data: List[ProductSummary]
    pagination: PaginationMeta
