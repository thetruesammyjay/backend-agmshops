"""
AGM Store Builder - Test Configuration

Shared fixtures for all tests. Uses mocked database sessions
so no real database connection is needed.
"""

import os
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport

# Override env vars BEFORE importing app modules
os.environ.update({
    "NODE_ENV": "testing",
    "DB_HOST": "localhost",
    "DB_PORT": "3306",
    "DB_USER": "test_user",
    "DB_PASSWORD": "test_password",
    "DB_NAME": "test_db",
    "DB_SSL": "false",
    "JWT_SECRET": "test-secret-key-for-testing-only-1234567890",
    "JWT_ACCESS_EXPIRY": "15m",
    "JWT_REFRESH_EXPIRY": "7d",
    "MONNIFY_API_KEY": "test_monnify_key",
    "MONNIFY_SECRET_KEY": "test_monnify_secret",
    "MONNIFY_CONTRACT_CODE": "0000000000",
    "CLOUDINARY_CLOUD_NAME": "test_cloud",
    "CLOUDINARY_API_KEY": "test_key",
    "CLOUDINARY_API_SECRET": "test_secret",
    "SENDGRID_API_KEY": "test_sendgrid",
    "TERMII_API_KEY": "test_termii",
    "CORS_ORIGIN": "http://localhost:3000",
})

from app.core.security import create_access_token


@pytest.fixture
def mock_db_session():
    """Create a mocked async database session."""
    session = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    session.execute = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    return session


@pytest.fixture
def auth_headers():
    """Generate valid JWT Bearer headers for authenticated endpoint tests."""
    token = create_access_token(data={"sub": "test-user-id-123"})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_user_id():
    """Standard test user ID."""
    return "test-user-id-123"


@pytest.fixture
async def async_client(mock_db_session):
    """
    Create an async HTTP client for testing API endpoints.
    
    Overrides the database dependency with a mock session
    so tests don't need a real database connection.
    """
    from app.main import app
    from app.dependencies import get_db

    async def override_get_db():
        yield mock_db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
