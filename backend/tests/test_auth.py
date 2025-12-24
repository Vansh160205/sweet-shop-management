import pytest
from jose import jwt

def test_register_user_success(client):
    response = client.post("/api/auth/register", json={
        "email_address": "vanilla@example.com",
        "password": "SweetPass123!",
        "full_name": "Vanilla Lover"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["email_address"] == "vanilla@example.com"
    assert data["full_name"] == "Vanilla Lover"
    assert "user_id" in data
    assert data["is_administrator"] is False
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_missing_required_fields(client):
    response = client.post("/api/auth/register", json={
        "email_address": "test@example.com"
        # missing password and full_name
    })
    assert response.status_code == 422


def test_register_invalid_email_format(client):
    response = client.post("/api/auth/register", json={
        "email_address": "not-an-email",
        "password": "securepass123",
        "full_name": "Bad Email User"
    })
    assert response.status_code == 422


def test_register_password_too_short(client):
    response = client.post("/api/auth/register", json={
        "email_address": "short@example.com",
        "password": "short",  # Less than 8 chars
        "full_name": "Short Password User"
    })
    assert response.status_code == 422


def test_register_duplicate_email(client):
    payload = {
        "email_address": "duplicate@example.com",
        "password": "securepass123",
        "full_name": "First User"
    }
    r1 = client.post("/api/auth/register", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/api/auth/register", json=payload)
    assert r2.status_code == 409  # Will fail now → forces us to implement


def test_login_endpoint_exists(client):
    response = client.post("/api/auth/login", json={
        "email_address": "test@example.com",
        "password": "securepass123"
    })
    # Should not be 404 (endpoint must exist)
    assert response.status_code != 404


def test_login_returns_valid_jwt_with_user_id(client):
    # Register first
    client.post("/api/auth/register", json={
        "email_address": "jwt@test.com",
        "password": "MyStrongPass123",
        "full_name": "JWT User"
    })
    # Login with form data (OAuth2 standard)
    response = client.post("/api/auth/login", data={
        "username": "jwt@test.com",
        "password": "MyStrongPass123"
    })
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    
    # Decode and verify JWT claims
    token = token_data["access_token"]
    payload = jwt.decode(token, "super-secret-sweet-shop-key-2025", algorithms=["HS256"])
    assert payload["sub"] == "1"  # First user ID as string
    assert "exp" in payload


def test_protected_me_endpoint_requires_valid_token(client):
    # No token = 401
    response = client.get("/api/auth/me")
    assert response.status_code == 401
    
    # Invalid token = 401
    response = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid-token"})
    assert response.status_code == 401


def test_protected_me_returns_current_user(client):
    # Register
    client.post("/api/auth/register", json={
        "email_address": "protected@test.com",
        "password": "SecurePass123",
        "full_name": "Protected User"
    })
    
    # Login to get token
    login_response = client.post("/api/auth/login", data={
        "username": "protected@test.com",
        "password": "SecurePass123"
    })
    token = login_response.json()["access_token"]
    
    # Access protected route with token
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["email_address"] == "protected@test.com"
    assert data["full_name"] == "Protected User"
    assert data["is_administrator"] is False
    assert "user_id" in data

