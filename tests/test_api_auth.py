"""
Tests for authentication API endpoints.

Uses mocked AuthService to test the API layer independently
from the database.
"""

import pytest
from unittest.mock import patch, AsyncMock

from app.core.exceptions import ConflictError, AuthenticationError


# ── Register ──────────────────────────────────────────────────────


class TestRegisterEndpoint:
    @patch("app.api.v1.auth.AuthService")
    async def test_register_success(self, MockAuthService, async_client):
        mock_service = AsyncMock()
        mock_service.register.return_value = {
            "user": {
                "id": "new-user-id",
                "email": "new@example.com",
                "full_name": "New User",
                "phone": None,
                "email_verified": False,
                "phone_verified": False,
                "is_active": True,
                "has_completed_onboarding": False,
                "last_login_at": None,
                "created_at": "2026-02-21T00:00:00",
            },
            "tokens": {
                "accessToken": "mock-access-token",
                "refreshToken": "mock-refresh-token",
            },
        }
        MockAuthService.return_value = mock_service

        response = await async_client.post(
            "/api/v1/auth/register",
            json={
                "email": "new@example.com",
                "password": "SecurePass1",
                "full_name": "New User",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["user"]["email"] == "new@example.com"
        assert "accessToken" in data["data"]["tokens"]

    @patch("app.api.v1.auth.AuthService")
    async def test_register_duplicate_email(self, MockAuthService, async_client):
        mock_service = AsyncMock()
        mock_service.register.side_effect = ConflictError(
            message="Email already registered"
        )
        MockAuthService.return_value = mock_service

        response = await async_client.post(
            "/api/v1/auth/register",
            json={
                "email": "existing@example.com",
                "password": "SecurePass1",
                "full_name": "Existing User",
            },
        )

        assert response.status_code == 409

    async def test_register_invalid_password(self, async_client):
        """Password validation happens at the schema level (Pydantic)."""
        response = await async_client.post(
            "/api/v1/auth/register",
            json={
                "email": "user@example.com",
                "password": "weak",
                "full_name": "User Name",
            },
        )
        assert response.status_code == 422

    async def test_register_invalid_email(self, async_client):
        response = await async_client.post(
            "/api/v1/auth/register",
            json={
                "email": "not-an-email",
                "password": "SecurePass1",
                "full_name": "User Name",
            },
        )
        assert response.status_code == 422


# ── Login ─────────────────────────────────────────────────────────


class TestLoginEndpoint:
    @patch("app.api.v1.auth.AuthService")
    async def test_login_success(self, MockAuthService, async_client):
        mock_service = AsyncMock()
        mock_service.login.return_value = {
            "user": {
                "id": "user-123",
                "email": "user@example.com",
                "full_name": "Test User",
                "phone": None,
                "email_verified": True,
                "phone_verified": False,
                "is_active": True,
                "has_completed_onboarding": True,
                "last_login_at": "2026-02-21T00:00:00",
                "created_at": "2026-01-01T00:00:00",
            },
            "tokens": {
                "accessToken": "mock-access-token",
                "refreshToken": "mock-refresh-token",
            },
        }
        MockAuthService.return_value = mock_service

        response = await async_client.post(
            "/api/v1/auth/login",
            json={
                "email": "user@example.com",
                "password": "CorrectPass1",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Login successful"

    @patch("app.api.v1.auth.AuthService")
    async def test_login_wrong_password(self, MockAuthService, async_client):
        mock_service = AsyncMock()
        mock_service.login.side_effect = AuthenticationError(
            message="Invalid email or password"
        )
        MockAuthService.return_value = mock_service

        response = await async_client.post(
            "/api/v1/auth/login",
            json={
                "email": "user@example.com",
                "password": "WrongPass1",
            },
        )

        assert response.status_code == 401


# ── Logout ────────────────────────────────────────────────────────


class TestLogoutEndpoint:
    @patch("app.api.v1.auth.AuthService")
    async def test_logout_success(self, MockAuthService, async_client, auth_headers):
        mock_service = AsyncMock()
        mock_service.logout.return_value = None
        MockAuthService.return_value = mock_service

        response = await async_client.post(
            "/api/v1/auth/logout",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Logged out successfully"

    async def test_logout_no_token(self, async_client):
        response = await async_client.post("/api/v1/auth/logout")
        assert response.status_code == 401
