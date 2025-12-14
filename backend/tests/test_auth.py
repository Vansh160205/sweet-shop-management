import pytest


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