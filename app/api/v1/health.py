"""
AGM Store Builder - Health Check Endpoints

Health check and version endpoints for monitoring.
"""

from datetime import datetime, timezone
import time
from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()

# Application start time for uptime calculation
_start_time = time.time()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns the health status of the API with database connectivity.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime": time.time() - _start_time,
        "environment": settings.APP_ENV,
        "version": settings.APP_VERSION,
        "database": "connected",  # TODO: Add actual DB health check
    }


@router.get("/version")
async def get_version():
    """
    Get API version information.
    """
    return {
        "success": True,
        "data": {
            "version": settings.APP_VERSION,
            "apiVersion": "v1",
            "environment": settings.APP_ENV,
            "buildDate": "2025-01-20",
        },
    }
