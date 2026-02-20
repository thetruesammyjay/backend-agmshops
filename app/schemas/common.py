"""
AGM Store Builder - Common Schemas

Shared Pydantic schemas for responses and pagination.
"""

from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field


T = TypeVar("T")


class BaseResponse(BaseModel):
    """Base response schema."""
    success: bool = True
    message: Optional[str] = None


class MessageResponse(BaseModel):
    """Simple message response."""
    success: bool = True
    message: str


class DataResponse(BaseResponse, Generic[T]):
    """Response with data payload."""
    data: T


class ErrorResponse(BaseModel):
    """Error response schema."""
    success: bool = False
    message: str
    statusCode: int
    details: Optional[Dict[str, Any]] = None


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    page: int
    limit: int
    total: int
    pages: int
    hasMore: bool = False


class PaginatedResponse(BaseResponse, Generic[T]):
    """Paginated response with data and pagination info."""
    data: List[T]
    pagination: PaginationMeta


class PaginationParams(BaseModel):
    """Pagination query parameters."""
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
