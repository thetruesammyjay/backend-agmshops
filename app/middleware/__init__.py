"""
AGM Store Builder - Middleware Module

Exports all middleware components for the application.
"""

from app.middleware.error_handler import (
    setup_exception_handlers,
    create_error_response,
)
from app.middleware.logging import setup_logging
from app.middleware.cors import setup_cors
from app.middleware.rate_limit import (
    limiter,
    setup_rate_limiting,
    rate_limit_exceeded_handler,
)

__all__ = [
    # Error handling
    "setup_exception_handlers",
    "create_error_response",
    # Logging
    "setup_logging",
    # CORS
    "setup_cors",
    # Rate limiting
    "limiter",
    "setup_rate_limiting",
    "rate_limit_exceeded_handler",
]
