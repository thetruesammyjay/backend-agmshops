"""
AGM Store Builder - Schemas Module

Exports all Pydantic schemas for the application.
"""

from app.schemas.common import (
    BaseResponse,
    MessageResponse,
    DataResponse,
    ErrorResponse,
    PaginationMeta,
    PaginatedResponse,
    PaginationParams,
)

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    VerifyOTPRequest,
    ResetPasswordRequest,
    ResendVerificationRequest,
    AuthResponse,
    TokenResponse,
    VerifyOTPResponse,
)

from app.schemas.user import (
    UserBase,
    UserResponse,
    UserProfileResponse,
    UpdateProfileRequest,
    ChangePasswordRequest,
)

from app.schemas.store import (
    CreateStoreRequest,
    UpdateStoreRequest,
    StoreResponse,
    StoreDetailResponse,
    StoreListResponse,
    CheckUsernameResponse,
    ToggleStatusRequest,
)

from app.schemas.product import (
    CreateProductRequest,
    UpdateProductRequest,
    ProductResponse,
    ProductDetailResponse,
    ProductListResponse,
    UpdateStockRequest,
    ToggleProductStatusRequest,
    BulkUpdateRequest,
)

from app.schemas.order import (
    CreateOrderRequest,
    OrderResponse,
    OrderDetailResponse,
    OrderListResponse,
    OrderTrackingResponse,
    UpdateOrderStatusRequest,
)

from app.schemas.payment import (
    BankAccountRequest,
    BankAccountResponse,
    BankAccountListResponse,
    BankListResponse,
    PaymentVerifyResponse,
    PaymentDetailResponse,
    PaymentReinitializeResponse,
)

from app.schemas.analytics import (
    DashboardResponse,
    RevenueResponse,
    OrderStatsResponse,
    ProductPerformanceResponse,
    CustomerAnalyticsResponse,
)

from app.schemas.upload import (
    UploadResponse,
    MultiUploadResponse,
)

__all__ = [
    # Common
    "BaseResponse",
    "MessageResponse",
    "DataResponse",
    "ErrorResponse",
    "PaginationMeta",
    "PaginatedResponse",
    "PaginationParams",
    # Auth
    "RegisterRequest",
    "LoginRequest",
    "RefreshTokenRequest",
    "ForgotPasswordRequest",
    "VerifyOTPRequest",
    "ResetPasswordRequest",
    "ResendVerificationRequest",
    "AuthResponse",
    "TokenResponse",
    "VerifyOTPResponse",
    # User
    "UserBase",
    "UserResponse",
    "UserProfileResponse",
    "UpdateProfileRequest",
    "ChangePasswordRequest",
    # Store
    "CreateStoreRequest",
    "UpdateStoreRequest",
    "StoreResponse",
    "StoreDetailResponse",
    "StoreListResponse",
    "CheckUsernameResponse",
    "ToggleStatusRequest",
    # Product
    "CreateProductRequest",
    "UpdateProductRequest",
    "ProductResponse",
    "ProductDetailResponse",
    "ProductListResponse",
    "UpdateStockRequest",
    "ToggleProductStatusRequest",
    "BulkUpdateRequest",
    # Order
    "CreateOrderRequest",
    "OrderResponse",
    "OrderDetailResponse",
    "OrderListResponse",
    "OrderTrackingResponse",
    "UpdateOrderStatusRequest",
    # Payment
    "BankAccountRequest",
    "BankAccountResponse",
    "BankAccountListResponse",
    "BankListResponse",
    "PaymentVerifyResponse",
    "PaymentDetailResponse",
    "PaymentReinitializeResponse",
    # Analytics
    "DashboardResponse",
    "RevenueResponse",
    "OrderStatsResponse",
    "ProductPerformanceResponse",
    "CustomerAnalyticsResponse",
    # Upload
    "UploadResponse",
    "MultiUploadResponse",
]
