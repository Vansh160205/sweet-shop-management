# backend/tests/test_auth.py
import pytest
from httpx import AsyncClient
from app.main import app  # Will fail to import → perfect RED


@pytest.mark.asyncio
async def test_register_user_success():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/auth/register", json={
            "email_address": "test@example.com",
            "password": "strongpassword123",
            "full_name": "Test User"
        })
        assert response.status_code == 201
        assert response.json()["email_address"] == "test@example.com"


@pytest.mark.asyncio
async def test_register_user_duplicate_email():
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post("/api/auth/register", json={
            "email_address": "duplicate@example.com",
            "password": "securepass123",
            "full_name": "First User"
        })
        response = await client.post("/api/auth/register", json={
            "email_address": "duplicate@example.com",
            "password": "securepass123",
            "full_name": "Second User"
        })
        assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_user_invalid_email():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/auth/register", json={
            "email_address": "not-an-email",
            "password": "securepass123",
            "full_name": "Bad Email User"
        })
        assert response.status_code == 422