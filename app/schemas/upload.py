"""
AGM Store Builder - Upload Schemas

Pydantic schemas for file upload responses.
"""

from typing import Optional, List
from pydantic import BaseModel


class UploadedImage(BaseModel):
    """Uploaded image data."""
    url: str
    secure_url: str
    public_id: str
    width: Optional[int] = None
    height: Optional[int] = None
    format: Optional[str] = None
    resource_type: str = "image"


class UploadResponse(BaseModel):
    """Single image upload response."""
    success: bool = True
    data: UploadedImage


class MultiUploadResponse(BaseModel):
    """Multiple images upload response."""
    success: bool = True
    data: List[UploadedImage]
