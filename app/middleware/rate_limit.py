"""
AGM Store Builder - Rate Limiting Middleware

Rate limiting using SlowAPI for request throttling.
"""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings


# Create limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"],
)


def get_rate_limit_key(request: Request) -> str:
    """
    Get the rate limit key for a request.
    
    Uses the client's IP address as the key.
    For authenticated users, could use user ID.
    
    Args:
        request: FastAPI Request object
        
    Returns:
        Rate limit key string
    """
    # Get client IP
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def rate_limit_exceeded_handler(
    request: Request,
    exc: RateLimitExceeded,
) -> JSONResponse:
    """
    Custom handler for rate limit exceeded errors.
    
    Returns a JSON response with retry information.
    """
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "message": "Too many requests. Please try again later.",
            "statusCode": 429,
            "details": {
                "retry_after": 60,
            },
        },
        headers={
            "Retry-After": "60",
            "X-RateLimit-Limit": str(settings.RATE_LIMIT_PER_MINUTE),
            "X-RateLimit-Remaining": "0",
        },
    )


def setup_rate_limiting(app: FastAPI) -> None:
    """
    Configure rate limiting for the application.
    
    Args:
        app: FastAPI application instance
    """
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)  # type: ignore[arg-type]
