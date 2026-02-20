"""
AGM Store Builder - API Dependencies

Common dependencies used across API endpoints.
Re-exports from app.dependencies for convenience.
"""

from app.dependencies import (
    get_db,
    DatabaseSession,
    get_current_user_id,
    CurrentUserId,
    get_optional_user_id,
    OptionalUserId,
    RoleChecker,
    require_admin,
    RequireAdmin,
    require_super_admin,
    RequireSuperAdmin,
    get_client_ip,
    ClientIP,
)

__all__ = [
    "get_db",
    "DatabaseSession",
    "get_current_user_id",
    "CurrentUserId",
    "get_optional_user_id",
    "OptionalUserId",
    "RoleChecker",
    "require_admin",
    "RequireAdmin",
    "require_super_admin",
    "RequireSuperAdmin",
    "get_client_ip",
    "ClientIP",
]
