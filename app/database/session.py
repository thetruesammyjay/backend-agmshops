"""
AGM Store Builder - Database Session Management

Async session factory for SQLAlchemy ORM operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.database.connection import get_engine


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    """
    Create an async session maker factory.
    
    Returns:
        async_sessionmaker: Factory for creating async sessions
    """
    return async_sessionmaker(
        bind=get_engine(),
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


# Create a session maker instance
async_session_maker = get_session_maker()


async def get_session() -> AsyncSession:
    """
    Get a new async database session.
    
    This should typically be used with async context manager.
    For dependency injection, use the get_db dependency instead.
    
    Returns:
        AsyncSession: New database session
    """
    return async_session_maker()
