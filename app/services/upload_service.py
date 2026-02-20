"""
AGM Store Builder - Upload Service

Image upload service that stores images as base64 data URLs.
No external storage services required - images are stored directly in the database.
"""

import base64
import uuid
from typing import Dict, Any, Optional
from loguru import logger

from app.core.exceptions import FileUploadError


# Allowed MIME types and their extensions
ALLOWED_MIME_TYPES = {
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/gif": "gif",
    "image/webp": "webp",
}

# Max file size: 5MB
MAX_FILE_SIZE = 5 * 1024 * 1024


class UploadService:
    """
    Upload service that converts images to base64 data URLs.
    
    Images are stored as data URLs directly in the database JSON columns.
    This removes the dependency on external storage services like Cloudinary.
    """
    
    def __init__(self):
        pass
    
    def _get_mime_type(self, filename: str, content: bytes) -> str:
        """Detect MIME type from file extension or magic bytes."""
        # Check by extension first
        ext = filename.lower().split('.')[-1] if '.' in filename else ''
        extension_map = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp',
        }
        
        if ext in extension_map:
            return extension_map[ext]
        
        # Check by magic bytes
        if content[:8] == b'\x89PNG\r\n\x1a\n':
            return 'image/png'
        elif content[:2] == b'\xff\xd8':
            return 'image/jpeg'
        elif content[:6] in (b'GIF87a', b'GIF89a'):
            return 'image/gif'
        elif content[:4] == b'RIFF' and content[8:12] == b'WEBP':
            return 'image/webp'
        
        # Default to JPEG
        return 'image/jpeg'
    
    def _validate_image(self, content: bytes, filename: str) -> str:
        """Validate image and return MIME type."""
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            raise FileUploadError(
                message=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB",
                details={"size": len(content), "max_size": MAX_FILE_SIZE}
            )
        
        # Get and validate MIME type
        mime_type = self._get_mime_type(filename, content)
        if mime_type not in ALLOWED_MIME_TYPES:
            raise FileUploadError(
                message="Invalid file type. Allowed: JPEG, PNG, GIF, WebP",
                details={"mime_type": mime_type}
            )
        
        return mime_type
    
    async def upload_image(
        self,
        file_content: bytes,
        filename: str,
        user_id: Optional[str] = None,
        folder: str = "products",
    ) -> Dict[str, Any]:
        """
        Convert an image to base64 data URL.
        
        Args:
            file_content: Image file bytes
            filename: Original filename
            user_id: Optional user ID (not used, kept for API compatibility)
            folder: Category folder (not used, kept for API compatibility)
            
        Returns:
            Upload result with data URL
            
        Raises:
            FileUploadError: If validation fails
        """
        try:
            # Validate image
            mime_type = self._validate_image(file_content, filename)
            
            # Convert to base64 data URL
            base64_data = base64.b64encode(file_content).decode('utf-8')
            data_url = f"data:{mime_type};base64,{base64_data}"
            
            # Generate a unique ID for tracking
            public_id = f"{folder}/{uuid.uuid4().hex[:12]}"
            
            logger.info(f"Image converted to base64: {filename} ({len(file_content)} bytes)")
            
            return {
                "url": data_url,
                "secure_url": data_url,
                "public_id": public_id,
                "width": None,  # Not computed for performance
                "height": None,
                "format": ALLOWED_MIME_TYPES.get(mime_type, "jpg"),
                "resource_type": "image",
                "size": len(file_content),
            }
            
        except FileUploadError:
            raise
        except Exception as e:
            logger.error(f"Upload error: {e}")
            raise FileUploadError(
                message="Failed to process image",
                details={"error": str(e)},
            )
    
    async def delete_image(
        self,
        public_id: str,
        user_id: Optional[str] = None,
    ) -> bool:
        """
        Delete an image (no-op for base64 storage).
        
        Since images are stored as data URLs in the database,
        deletion happens when the record is deleted.
        
        Returns:
            Always True
        """
        logger.info(f"Image delete requested: {public_id} (no-op for base64 storage)")
        return True
    
    async def upload_avatar(
        self,
        file_content: bytes,
        user_id: str,
    ) -> Dict[str, Any]:
        """Upload a user avatar."""
        return await self.upload_image(
            file_content=file_content,
            filename=f"avatar_{user_id}.jpg",
            user_id=user_id,
            folder="avatars",
        )
    
    async def upload_store_logo(
        self,
        file_content: bytes,
        store_id: str,
    ) -> Dict[str, Any]:
        """Upload a store logo."""
        return await self.upload_image(
            file_content=file_content,
            filename=f"logo_{store_id}.png",
            user_id=None,
            folder="logos",
        )
    
    async def upload_store_banner(
        self,
        file_content: bytes,
        store_id: str,
    ) -> Dict[str, Any]:
        """Upload a store banner."""
        return await self.upload_image(
            file_content=file_content,
            filename=f"banner_{store_id}.jpg",
            user_id=None,
            folder="banners",
        )
