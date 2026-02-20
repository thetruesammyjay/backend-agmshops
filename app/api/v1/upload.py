"""
AGM Store Builder - Upload Endpoints

File upload endpoints for images using Cloudinary.
"""

from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user_id
from app.services.upload_service import UploadService
from app.schemas.upload import (
    UploadResponse,
    MultiUploadResponse,
)
from app.schemas.common import MessageResponse

router = APIRouter()

# Allowed image types
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_image(file: UploadFile) -> None:
    """Validate uploaded image file."""
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_TYPES)}",
        )


@router.post("/image", response_model=UploadResponse)
async def upload_image(
    image: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload a single image to Cloudinary.
    
    Accepts JPG, PNG, WEBP, and GIF up to 5MB.
    """
    validate_image(image)
    
    # Read file content
    content = await image.read()
    
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 5MB limit",
        )
    
    upload_service = UploadService()
    result = await upload_service.upload_image(
        file_content=content,
        filename=image.filename or "image.jpg",
        user_id=user_id,
    )
    
    return {
        "success": True,
        "data": result,
    }


@router.post("/images", response_model=MultiUploadResponse)
async def upload_multiple_images(
    images: List[UploadFile] = File(...),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload multiple images to Cloudinary (max 5).
    
    Accepts JPG, PNG, WEBP, and GIF up to 5MB each.
    """
    if len(images) > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 5 images allowed per upload",
        )
    
    for image in images:
        validate_image(image)
    
    upload_service = UploadService()
    results = []
    
    for image in images:
        content = await image.read()
        
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File {image.filename} exceeds 5MB limit",
            )
        
        result = await upload_service.upload_image(
            file_content=content,
            filename=image.filename or "image.jpg",
            user_id=user_id,
        )
        results.append(result)
    
    return {
        "success": True,
        "data": results,
    }


@router.delete("/image/{public_id:path}", response_model=MessageResponse)
async def delete_image(
    public_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete an image from Cloudinary.
    
    Removes the image by its public ID.
    """
    upload_service = UploadService()
    await upload_service.delete_image(public_id, user_id)
    
    return {
        "success": True,
        "message": "Image deleted successfully",
    }
