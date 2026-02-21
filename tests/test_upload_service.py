"""
Tests for app.services.upload_service — image upload to base64.
"""

import pytest

from app.services.upload_service import UploadService, MAX_FILE_SIZE
from app.core.exceptions import FileUploadError


@pytest.fixture
def upload_service():
    return UploadService()


# Minimal valid JPEG (2x2 white pixel)
TINY_JPEG = (
    b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
    b"\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t"
    b"\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a"
    b"\x1f\x1e\x1d\x1a\x1c\x1c $.\' \",#\x1c\x1c(7),01444\x1f\'9=82<.342"
    b"\xff\xc0\x00\x0b\x08\x00\x02\x00\x02\x01\x01\x11\x00"
    b"\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b"
    b"\xff\xda\x00\x08\x01\x01\x00\x00?\x00T\xdb\x9e\xa7\x13(\xa0\x02\x80\x0f\xff\xd9"
)

# Minimal valid PNG header
TINY_PNG = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02"
    b"\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx"
    b"\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
)


# ── Upload Image ──────────────────────────────────────────────────


class TestUploadImage:
    async def test_valid_jpeg_upload(self, upload_service):
        result = await upload_service.upload_image(
            file_content=TINY_JPEG,
            filename="test.jpg",
        )
        assert result["url"].startswith("data:image/jpeg;base64,")
        assert result["secure_url"] == result["url"]
        assert result["resource_type"] == "image"
        assert result["size"] == len(TINY_JPEG)

    async def test_valid_png_upload(self, upload_service):
        result = await upload_service.upload_image(
            file_content=TINY_PNG,
            filename="test.png",
        )
        assert result["url"].startswith("data:image/png;base64,")

    async def test_custom_folder(self, upload_service):
        result = await upload_service.upload_image(
            file_content=TINY_JPEG,
            filename="product.jpg",
            folder="products",
        )
        assert result["public_id"].startswith("products/")

    async def test_file_too_large_raises(self, upload_service):
        large_content = b"\xff\xd8" + b"\x00" * (MAX_FILE_SIZE + 1)
        with pytest.raises(FileUploadError, match="too large"):
            await upload_service.upload_image(
                file_content=large_content,
                filename="huge.jpg",
            )

    async def test_unknown_content_defaults_to_jpeg(self, upload_service):
        """The service defaults unknown content to image/jpeg rather than rejecting."""
        result = await upload_service.upload_image(
            file_content=b"not-an-image-content-at-all",
            filename="test.txt",
        )
        assert result["url"].startswith("data:image/jpeg;base64,")


# ── Delete Image ──────────────────────────────────────────────────


class TestDeleteImage:
    async def test_delete_returns_true(self, upload_service):
        result = await upload_service.delete_image("products/abc123")
        assert result is True


# ── Convenience Methods ───────────────────────────────────────────


class TestConvenienceMethods:
    async def test_upload_avatar(self, upload_service):
        result = await upload_service.upload_avatar(
            file_content=TINY_JPEG,
            user_id="user-avatar-1",
        )
        assert result["public_id"].startswith("avatars/")

    async def test_upload_store_logo(self, upload_service):
        result = await upload_service.upload_store_logo(
            file_content=TINY_PNG,
            store_id="store-logo-1",
        )
        assert result["public_id"].startswith("logos/")

    async def test_upload_store_banner(self, upload_service):
        result = await upload_service.upload_banner(
            file_content=TINY_JPEG,
            store_id="store-banner-1",
        ) if hasattr(upload_service, "upload_banner") else (
            await upload_service.upload_store_banner(
                file_content=TINY_JPEG,
                store_id="store-banner-1",
            )
        )
        assert result["public_id"].startswith("banners/")
