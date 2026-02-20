"""
AGM Store Builder - Database Connection

MySQL async connection pool management using SQLAlchemy 2.0.
"""

import ssl
from typing import Optional
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool
from loguru import logger

from app.core.config import settings

# Global engine instance
_engine: Optional[AsyncEngine] = None


def get_engine() -> AsyncEngine:
    """
    Get or create the async database engine.
    
    Uses a singleton pattern to ensure only one engine exists.
    
    Returns:
        AsyncEngine: SQLAlchemy async engine instance
    """
    global _engine
    
    if _engine is None:
        connect_args = {}
        if settings.DB_SSL:
            ssl_ctx = ssl.create_default_context()
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = ssl.CERT_NONE
            connect_args["ssl"] = ssl_ctx

        _engine = create_async_engine(
            settings.DATABASE_URL,
            poolclass=AsyncAdaptedQueuePool,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_recycle=settings.DB_POOL_RECYCLE,
            pool_pre_ping=True,
            echo=settings.APP_DEBUG and settings.APP_ENV == "development",
            connect_args=connect_args,
        )
    
    return _engine


async def init_database() -> None:
    """
    Initialize the database connection pool.
    
    Called during application startup to ensure the database
    is accessible and the connection pool is ready.
    """
    engine = get_engine()
    
    # Test the connection
    try:
        async with engine.connect() as conn:
            from sqlalchemy import text
            await conn.execute(text("SELECT 1"))
        logger.info(f"Connected to database: {settings.DB_NAME}@{settings.DB_HOST}")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise


async def close_database() -> None:
    """
    Close the database connection pool.
    
    Called during application shutdown to properly close all connections.
    """
    global _engine
    
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        logger.info("Database connection pool closed")
