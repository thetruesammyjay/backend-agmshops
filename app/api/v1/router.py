"""
AGM Store Builder - API v1 Router

Aggregates all v1 API routes into a single router.
"""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.stores import router as stores_router
from app.api.v1.products import router as products_router
from app.api.v1.orders import router as orders_router
from app.api.v1.payments import router as payments_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.upload import router as upload_router
from app.api.v1.webhooks import router as webhooks_router
from app.api.v1.health import router as health_router
from app.api.v1.customers import router as customers_router
from app.api.v1.settings import router as settings_router

# Create main API v1 router
api_v1_router = APIRouter()

# Include all sub-routers
api_v1_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)

api_v1_router.include_router(
    users_router,
    prefix="/users",
    tags=["Users"],
)

api_v1_router.include_router(
    stores_router,
    prefix="/stores",
    tags=["Stores"],
)

api_v1_router.include_router(
    products_router,
    prefix="/products",
    tags=["Products"],
)

api_v1_router.include_router(
    orders_router,
    prefix="/orders",
    tags=["Orders"],
)

api_v1_router.include_router(
    payments_router,
    prefix="/payments",
    tags=["Payments"],
)

api_v1_router.include_router(
    analytics_router,
    prefix="/analytics",
    tags=["Analytics"],
)

api_v1_router.include_router(
    upload_router,
    prefix="/upload",
    tags=["Upload"],
)

api_v1_router.include_router(
    webhooks_router,
    prefix="/webhooks",
    tags=["Webhooks"],
)

api_v1_router.include_router(
    health_router,
    tags=["Health"],
)

api_v1_router.include_router(
    customers_router,
    prefix="/dashboard",
    tags=["Dashboard"],
)

api_v1_router.include_router(
    settings_router,
    prefix="/settings",
    tags=["Settings"],
)
