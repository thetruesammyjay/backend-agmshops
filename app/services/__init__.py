"""
AGM Store Builder - Services Module

Exports all service classes for the application.
"""

from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.store_service import StoreService
from app.services.product_service import ProductService
from app.services.order_service import OrderService
from app.services.payment_service import PaymentService
from app.services.analytics_service import AnalyticsService
from app.services.upload_service import UploadService
from app.services.otp_service import OTPService
from app.services.email_service import EmailService
from app.services.monnify_service import MonnifyService

__all__ = [
    "AuthService",
    "UserService",
    "StoreService",
    "ProductService",
    "OrderService",
    "PaymentService",
    "AnalyticsService",
    "UploadService",
    "OTPService",
    "EmailService",
    "MonnifyService",
]
