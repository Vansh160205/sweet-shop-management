import pytest


# ==================== HELPER FUNCTION ====================

def get_auth_header(client, email="admin@sweetshop.com", password="AdminPass123", is_admin=True):
    """Helper to register, login and get auth header."""
    client.post("/api/auth/register", json={
        "email_address": email,
        "password": password,
        "full_name": "Test User",
        "is_administrator": is_admin
    })
    response = client.post("/api/auth/login", data={
        "username": email,
        "password": password
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ==================== CREATE SWEET TESTS ====================

def test_create_sweet_success(client):
    headers = get_auth_header(client)
    response = client.post("/api/sweets", json={
        "sweet_name": "Chocolate Truffle",
        "sweet_category": "Chocolate",
        "sweet_price": 5.99,
        "quantity_in_stock": 100,
        "sweet_description": "Delicious dark chocolate truffle"
    }, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["sweet_name"] == "Chocolate Truffle"
    assert data["sweet_category"] == "Chocolate"
    assert data["sweet_price"] == 5.99
    assert data["quantity_in_stock"] == 100
    assert "sweet_id" in data


def test_create_sweet_requires_authentication(client):
    response = client.post("/api/sweets", json={
        "sweet_name": "Test Sweet",
        "sweet_category": "Test",
        "sweet_price": 1.99,
        "quantity_in_stock": 10
    })
    assert response.status_code == 401


def test_create_sweet_validation_error(client):
    headers = get_auth_header(client)
    # Missing required fields
    response = client.post("/api/sweets", json={
        "sweet_name": "Incomplete Sweet"
    }, headers=headers)
    assert response.status_code == 422


def test_create_sweet_invalid_price(client):
    headers = get_auth_header(client)
    response = client.post("/api/sweets", json={
        "sweet_name": "Bad Price Sweet",
        "sweet_category": "Test",
        "sweet_price": -5.00,  # Negative price
        "quantity_in_stock": 10
    }, headers=headers)
    assert response.status_code == 422


def test_create_sweet_invalid_quantity(client):
    headers = get_auth_header(client)
    response = client.post("/api/sweets", json={
        "sweet_name": "Bad Quantity Sweet",
        "sweet_category": "Test",
        "sweet_price": 5.00,
        "quantity_in_stock": -10  # Negative quantity
    }, headers=headers)
    assert response.status_code == 422


# ==================== GET ALL SWEETS TESTS ====================

def test_get_all_sweets_success(client):
    headers = get_auth_header(client)
    # Create some sweets first
    client.post("/api/sweets", json={
        "sweet_name": "Candy 1",
        "sweet_category": "Candy",
        "sweet_price": 1.99,
        "quantity_in_stock": 50
    }, headers=headers)
    client.post("/api/sweets", json={
        "sweet_name": "Candy 2",
        "sweet_category": "Candy",
        "sweet_price": 2.99,
        "quantity_in_stock": 30
    }, headers=headers)
    
    response = client.get("/api/sweets", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_all_sweets_requires_authentication(client):
    response = client.get("/api/sweets")
    assert response.status_code == 401


def test_get_all_sweets_empty_list(client):
    headers = get_auth_header(client)
    response = client.get("/api/sweets", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


# ==================== SEARCH SWEETS TESTS ====================

def test_search_sweets_by_name(client):
    headers = get_auth_header(client)
    client.post("/api/sweets", json={
        "sweet_name": "Chocolate Bar",
        "sweet_category": "Chocolate",
        "sweet_price": 3.99,
        "quantity_in_stock": 25
    }, headers=headers)
    client.post("/api/sweets", json={
        "sweet_name": "Vanilla Fudge",
        "sweet_category": "Fudge",
        "sweet_price": 4.99,
        "quantity_in_stock": 15
    }, headers=headers)
    
    response = client.get("/api/sweets/search?name=Chocolate", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["sweet_name"] == "Chocolate Bar"


def test_search_sweets_by_category(client):
    headers = get_auth_header(client)
    client.post("/api/sweets", json={
        "sweet_name": "Gummy Bear",
        "sweet_category": "Gummy",
        "sweet_price": 2.99,
        "quantity_in_stock": 100
    }, headers=headers)
    client.post("/api/sweets", json={
        "sweet_name": "Gummy Worm",
        "sweet_category": "Gummy",
        "sweet_price": 2.49,
        "quantity_in_stock": 80
    }, headers=headers)
    
    response = client.get("/api/sweets/search?category=Gummy", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_search_sweets_by_price_range(client):
    headers = get_auth_header(client)
    client.post("/api/sweets", json={
        "sweet_name": "Cheap Candy",
        "sweet_category": "Candy",
        "sweet_price": 1.00,
        "quantity_in_stock": 200
    }, headers=headers)
    client.post("/api/sweets", json={
        "sweet_name": "Premium Chocolate",
        "sweet_category": "Chocolate",
        "sweet_price": 15.00,
        "quantity_in_stock": 10
    }, headers=headers)
    
    response = client.get("/api/sweets/search?min_price=10&max_price=20", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["sweet_name"] == "Premium Chocolate"


def test_search_sweets_requires_authentication(client):
    response = client.get("/api/sweets/search?name=Test")
    assert response.status_code == 401


# ==================== UPDATE SWEET TESTS ====================

def test_update_sweet_success(client):
    headers = get_auth_header(client)
    # Create a sweet first
    create_response = client.post("/api/sweets", json={
        "sweet_name": "Original Name",
        "sweet_category": "Original",
        "sweet_price": 5.00,
        "quantity_in_stock": 50
    }, headers=headers)
    sweet_id = create_response.json()["sweet_id"]
    
    # Update it
    response = client.put(f"/api/sweets/{sweet_id}", json={
        "sweet_name": "Updated Name",
        "sweet_price": 7.99
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["sweet_name"] == "Updated Name"
    assert data["sweet_price"] == 7.99
    assert data["sweet_category"] == "Original"  # Unchanged


def test_update_sweet_not_found(client):
    headers = get_auth_header(client)
    response = client.put("/api/sweets/9999", json={
        "sweet_name": "Ghost Sweet"
    }, headers=headers)
    assert response.status_code == 404


def test_update_sweet_requires_authentication(client):
    response = client.put("/api/sweets/1", json={
        "sweet_name": "Hacker Sweet"
    })
    assert response.status_code == 401


# ==================== DELETE SWEET TESTS (ADMIN ONLY) ====================

def test_delete_sweet_admin_success(client):
    headers = get_auth_header(client, is_admin=True)
    # Create a sweet
    create_response = client.post("/api/sweets", json={
        "sweet_name": "Delete Me",
        "sweet_category": "Temporary",
        "sweet_price": 1.00,
        "quantity_in_stock": 1
    }, headers=headers)
    sweet_id = create_response.json()["sweet_id"]
    
    # Delete it
    response = client.delete(f"/api/sweets/{sweet_id}", headers=headers)
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get("/api/sweets", headers=headers)
    sweets = get_response.json()
    assert all(s["sweet_id"] != sweet_id for s in sweets)


def test_delete_sweet_non_admin_forbidden(client):
    # Create as admin
    admin_headers = get_auth_header(client, email="admin@test.com", is_admin=True)
    create_response = client.post("/api/sweets", json={
        "sweet_name": "Protected Sweet",
        "sweet_category": "Protected",
        "sweet_price": 10.00,
        "quantity_in_stock": 5
    }, headers=admin_headers)
    sweet_id = create_response.json()["sweet_id"]
    
    # Try to delete as non-admin
    user_headers = get_auth_header(client, email="user@test.com", is_admin=False)
    response = client.delete(f"/api/sweets/{sweet_id}", headers=user_headers)
    assert response.status_code == 403


def test_delete_sweet_not_found(client):
    headers = get_auth_header(client, is_admin=True)
    response = client.delete("/api/sweets/9999", headers=headers)
    assert response.status_code == 404


def test_delete_sweet_requires_authentication(client):
    response = client.delete("/api/sweets/1")
    assert response.status_code == 401