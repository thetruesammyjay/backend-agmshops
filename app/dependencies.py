"""
AGM Store Builder - Dependency Injection

FastAPI dependency injection functions for database sessions, 
authentication, rate limiting, and other shared dependencies.
"""

from typing import Annotated, AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import verify_access_token
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.constants import UserRole
from app.database.session import async_session_maker

# HTTP Bearer security scheme
security = HTTPBearer(auto_error=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get an async database session.
    
    Yields an async SQLAlchemy session and ensures proper cleanup.
    
    Yields:
        AsyncSession: Database session
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


# Type alias for database session dependency
DatabaseSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> str:
    """
    Dependency to get the current user's ID from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials from request
        
    Returns:
        User ID string extracted from the token
        
    Raises:
        HTTPException: If token is missing or invalid
    """
    from loguru import logger
    
    if credentials is None:
        logger.warning("Auth failed: No credentials provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user_id = verify_access_token(credentials.credentials)
        logger.debug(f"Auth successful for user: {user_id}")
        return user_id
    except Exception as e:
        logger.warning(f"Auth failed: Invalid token - {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Type alias for current user dependency
CurrentUserId = Annotated[str, Depends(get_current_user_id)]


async def get_optional_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[str]:
    """
    Dependency to optionally get the current user's ID.
    
    Returns None if no valid token is provided instead of raising an error.
    Useful for endpoints that work for both authenticated and anonymous users.
    
    Args:
        credentials: HTTP Bearer credentials from request
        
    Returns:
        User ID string if authenticated, None otherwise
    """
    if credentials is None:
        return None
    
    try:
        return verify_access_token(credentials.credentials)
    except Exception:
        return None


# Type alias for optional user dependency
OptionalUserId = Annotated[Optional[str], Depends(get_optional_user_id)]


class RoleChecker:
    """
    Dependency class to check if user has required role(s).
    
    Usage:
        @app.get("/admin-only")
        def admin_endpoint(
            user_id: CurrentUserId,
            _: bool = Depends(RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
        ):
            ...
    """
    
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles
    
    async def __call__(
        self,
        db: DatabaseSession,
        user_id: CurrentUserId,
    ) -> bool:
        """
        Check if the current user has one of the allowed roles.
        
        This is a placeholder - actual implementation needs the User model.
        """
        # Import here to avoid circular imports
        from app.repositories.user_repository import UserRepository
        
        user_repo = UserRepository(db)
        user = await user_repo.get_by_id(user_id)
        
        if user is None:
            raise AuthenticationError(message="User not found")
        
        if user.role not in [role.value for role in self.allowed_roles]:
            raise AuthorizationError(
                message="You don't have permission to access this resource"
            )
        
        return True


# Convenience dependency for admin-only endpoints
require_admin = RoleChecker([UserRole.ADMIN, UserRole.SUPER_ADMIN])
RequireAdmin = Annotated[bool, Depends(require_admin)]

# Convenience dependency for super-admin-only endpoints
require_super_admin = RoleChecker([UserRole.SUPER_ADMIN])
RequireSuperAdmin = Annotated[bool, Depends(require_super_admin)]


def get_client_ip(request: Request) -> str:
    """
    Get the client's IP address from the request.
    
    Handles X-Forwarded-For header for requests behind proxies.
    
    Args:
        request: FastAPI Request object
        
    Returns:
        Client IP address string
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # Return the first IP in the chain (original client)
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


ClientIP = Annotated[str, Depends(get_client_ip)]
