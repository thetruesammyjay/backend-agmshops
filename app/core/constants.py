"""
AGM Store Builder - Application Constants

Centralized constants used throughout the application.
"""

from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class StoreTemplate(str, Enum):
    """Store template types."""
    PRODUCTS = "products"
    BOOKINGS = "bookings"
    PORTFOLIO = "portfolio"


class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    EXPIRED = "expired"
    REFUNDED = "refunded"


class PaymentMethod(str, Enum):
    """Payment method enumeration."""
    BANK_TRANSFER = "bank_transfer"
    CARD = "card"
    USSD = "ussd"


class OTPType(str, Enum):
    """OTP type enumeration."""
    EMAIL = "email"
    PHONE = "phone"
    PASSWORD_RESET = "password_reset"
    LOGIN = "login"


class ProfileVisibility(str, Enum):
    """Profile visibility options."""
    PUBLIC = "public"
    PRIVATE = "private"


# Order status transitions (valid next statuses)
ORDER_STATUS_TRANSITIONS = {
    OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
    OrderStatus.CONFIRMED: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
    OrderStatus.PROCESSING: [OrderStatus.SHIPPED],
    OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
    OrderStatus.DELIVERED: [OrderStatus.FULFILLED],
    OrderStatus.FULFILLED: [],
    OrderStatus.CANCELLED: [],
}


# Nigerian States
NIGERIAN_STATES = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue",
    "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu",
    "FCT", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi",
    "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun",
    "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara",
]


# Product categories (common e-commerce categories)
PRODUCT_CATEGORIES = [
    "fashion",
    "electronics",
    "food_beverages",
    "health_beauty",
    "home_furniture",
    "phones_tablets",
    "computing",
    "sports_fitness",
    "books_media",
    "toys_games",
    "jewelry_accessories",
    "automotive",
    "services",
    "other",
]


# Store categories
STORE_CATEGORIES = [
    "fashion",
    "electronics",
    "food_restaurant",
    "health_beauty",
    "home_decor",
    "services",
    "art_crafts",
    "other",
]


# File upload limits
MAX_IMAGE_SIZE_MB = 5
MAX_IMAGES_PER_PRODUCT = 10
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]


# Pagination defaults
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


# Nigerian phone number regex
NIGERIAN_PHONE_REGEX = r"^(\+234|234|0)[789]\d{9}$"


# Password requirements
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_DIGIT = True


# API versioning
API_V1_PREFIX = "/api/v1"
