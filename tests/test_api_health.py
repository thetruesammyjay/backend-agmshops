"""
Tests for health and root API endpoints.
"""

import pytest


class TestRootEndpoint:
    async def test_root_returns_200(self, async_client):
        response = await async_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "AGM Store Builder" in data["message"]

    async def test_root_includes_version(self, async_client):
        response = await async_client.get("/")
        data = response.json()
        assert "version" in data


class TestHealthEndpoint:
    async def test_health_returns_200(self, async_client):
        response = await async_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    async def test_health_includes_environment(self, async_client):
        response = await async_client.get("/health")
        data = response.json()
        assert "environment" in data

    async def test_health_includes_version(self, async_client):
        response = await async_client.get("/health")
        data = response.json()
        assert "version" in data
