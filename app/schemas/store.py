"""
AGM Store Builder - Store Schemas

Pydantic schemas for store-related requests and responses.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class SocialLinks(BaseModel):
    """Store social links."""
    instagram: Optional[str] = None
    twitter: Optional[str] = None
    facebook: Optional[str] = None
    whatsapp: Optional[str] = None


class CreateStoreRequest(BaseModel):
    """Create store request."""
    name: str = Field(min_length=2, max_length=255)
    username: str = Field(min_length=3, max_length=100, pattern=r"^[a-z0-9_-]+$")
    description: Optional[str] = None
    category: Optional[str] = None
    logo: Optional[str] = None
    banner: Optional[str] = None
    social_links: Optional[Dict[str, str]] = None


class UpdateStoreRequest(BaseModel):
    """Update store request."""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    logo: Optional[str] = None
    banner: Optional[str] = None
    custom_colors: Optional[Dict[str, Any]] = None
    custom_fonts: Optional[Dict[str, Any]] = None
    social_links: Optional[Dict[str, str]] = None


class ToggleStatusRequest(BaseModel):
    """Toggle store status request."""
    is_active: bool


class StoreData(BaseModel):
    """Store data."""
    id: str
    user_id: str
    username: str
    display_name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    template_id: str = "products"
    category: Optional[str] = None
    custom_colors: Optional[Dict[str, Any]] = None
    custom_fonts: Optional[Dict[str, Any]] = None
    social_links: Optional[Dict[str, str]] = None
    is_active: bool = True
    created_at: str
    updated_at: Optional[str] = None


class StoreSummary(BaseModel):
    """Store summary with stats."""
    id: str
    name: str
    username: str
    logo: Optional[str] = None
    is_active: bool = True
    product_count: int = 0
    order_count: int = 0
    total_revenue: float = 0
    created_at: str


class StoreResponse(BaseModel):
    """Single store response."""
    success: bool = True
    data: StoreData


class StoreDetailResponse(BaseModel):
    """Store detail response."""
    success: bool = True
    data: StoreData
    message: Optional[str] = None


class StoreListResponse(BaseModel):
    """Store list response."""
    success: bool = True
    data: List[StoreSummary]


class UsernameAvailability(BaseModel):
    """Username availability data."""
    username: str
    available: bool
    suggestions: Optional[List[str]] = None


class CheckUsernameResponse(BaseModel):
    """Check username response."""
    success: bool = True
    data: UsernameAvailability
