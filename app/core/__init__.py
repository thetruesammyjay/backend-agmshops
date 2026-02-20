"""
AGM Store Builder - Core Module

Exports core utilities, settings, security, and exceptions.
"""

from app.core.config import Settings, get_settings, settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    create_tokens,
    decode_token,
    verify_access_token,
    verify_refresh_token,
    create_password_reset_token,
    verify_password_reset_token,
)
from app.core.exceptions import (
    AGMException,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ValidationError,
    ConflictError,
    BadRequestError,
    RateLimitError,
    PaymentError,
    ExternalServiceError,
    OTPError,
    TokenError,
    FileUploadError,
    DatabaseError,
)
from app.core.constants import (
    UserRole,
    StoreTemplate,
    OrderStatus,
    PaymentStatus,
    PaymentMethod,
    OTPType,
    ProfileVisibility,
    ORDER_STATUS_TRANSITIONS,
    NIGERIAN_STATES,
    PRODUCT_CATEGORIES,
    STORE_CATEGORIES,
    API_V1_PREFIX,
)

__all__ = [
    # Config
    "Settings",
    "get_settings",
    "settings",
    # Security
    "hash_password",
    "verify_password",
    "create_access_token",
    "create_refresh_token",
    "create_tokens",
    "decode_token",
    "verify_access_token",
    "verify_refresh_token",
    "create_password_reset_token",
    "verify_password_reset_token",
    # Exceptions
    "AGMException",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ValidationError",
    "ConflictError",
    "BadRequestError",
    "RateLimitError",
    "PaymentError",
    "ExternalServiceError",
    "OTPError",
    "TokenError",
    "FileUploadError",
    "DatabaseError",
    # Constants
    "UserRole",
    "StoreTemplate",
    "OrderStatus",
    "PaymentStatus",
    "PaymentMethod",
    "OTPType",
    "ProfileVisibility",
    "ORDER_STATUS_TRANSITIONS",
    "NIGERIAN_STATES",
    "PRODUCT_CATEGORIES",
    "STORE_CATEGORIES",
    "API_V1_PREFIX",
]
