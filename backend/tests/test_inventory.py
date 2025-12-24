import pytest


# ==================== HELPER FUNCTION ====================

def get_auth_header(client, email="admin@dg.in", password="admin123", is_admin=True):
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


def create_sweet(client, headers, name="Test Sweet", quantity=100):
    """Helper to create a sweet and return its ID."""
    response = client.post("/api/sweets", json={
        "sweet_name": name,
        "sweet_category": "Test",
        "sweet_price": 5.99,
        "quantity_in_stock": quantity,
        "sweet_description": "Test sweet"
    }, headers=headers)
    print(" Sweet Response : ",response.json())
    return response.json()["sweet_id"]


# ==================== PURCHASE TESTS ====================

def test_purchase_sweet_success(client):
    headers = get_auth_header(client)
    sweet_id = create_sweet(client, headers, quantity=100)
    
    response = client.post(f"/api/sweets/{sweet_id}/purchase", json={
        "quantity_to_purchase": 10
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Purchase successful"
    assert data["sweet_id"] == sweet_id
    assert data["previous_quantity"] == 100
    assert data["new_quantity"] == 90
    assert data["quantity_purchased"] == 10

def test_purchase_sweet_success_with_coupon(client):
    headers = get_auth_header(client)
    sweet_id = create_sweet(client, headers, quantity=100)
    
    response = client.post(f"/api/sweets/{sweet_id}/purchase", json={
        "quantity_to_purchase": 10,
        "coupon":"COUPON",
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Purchase successful"
    assert data["sweet_id"] == sweet_id
    assert data["previous_quantity"] == 100
    assert data["new_quantity"] == 90
    assert data["quantity_purchased"] == 10
    assert data["total_price"] == 59.9 
    assert data["discounted_price"] == 53.91



def test_purchase_sweet_reduces_stock(client):
    headers = get_auth_header(client)
    sweet_id = create_sweet(client, headers, quantity=50)
    
    # Purchase 20
    client.post(f"/api/sweets/{sweet_id}/purchase", json={
        "quantity_to_purchase": 20
    }, headers=headers)
    
    # Check updated stock
    response = client.get("/api/sweets", headers=headers)
    sweet = next(s for s in response.json() if s["sweet_id"] == sweet_id)
    assert sweet["quantity_in_stock"] == 30


def test_purchase_sweet_insufficient_stock(client):
    headers = get_auth_header(client)
    sweet_id = create_sweet(client, headers, quantity=5)
    
    response = client.post(f"/api/sweets/{sweet_id}/purchase", json={
        "quantity_to_purchase": 10
    }, headers=headers)
    
    assert response.status_code == 400
    assert "insufficient stock" in response.json()["detail"].lower()


def test_purchase_sweet_exact_stock(client):
    headers = get_auth_header(client)
    sweet_id = create_sweet(client, headers, quantity=15)
    
    response = client.post(f"/api/sweets/{sweet_id}/purchase", json={
        "quantity_to_purchase": 15
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["new_quantity"] == 0


def test_purchase_sweet_zero_quantity(client):
    headers = get_auth_header(client)
    sweet_id = create_sweet(client, headers, quantity=50)
    
    response = client.post(f"/api/sweets/{sweet_id}/purchase", json={
        "quantity_to_purchase": 0
    }, headers=headers)
    
    assert response.status_code == 422


def test_purchase_sweet_negative_quantity(client):
    headers = get_auth_header(client)
    sweet_id = create_sweet(client, headers, quantity=50)
    
    response = client.post(f"/api/sweets/{sweet_id}/purchase", json={
        "quantity_to_purchase": -5
    }, headers=headers)
    
    assert response.status_code == 422


def test_purchase_sweet_not_found(client):
    headers = get_auth_header(client)
    
    response = client.post("/api/sweets/9999/purchase", json={
        "quantity_to_purchase": 10
    }, headers=headers)
    
    assert response.status_code == 404


def test_purchase_sweet_requires_authentication(client):
    response = client.post("/api/sweets/1/purchase", json={
        "quantity_to_purchase": 10
    })
    
    assert response.status_code == 401


def test_purchase_from_out_of_stock_sweet(client):
    headers = get_auth_header(client)
    sweet_id = create_sweet(client, headers, quantity=0)
    
    response = client.post(f"/api/sweets/{sweet_id}/purchase", json={
        "quantity_to_purchase": 1
    }, headers=headers)
    
    assert response.status_code == 400


# ==================== RESTOCK TESTS ====================

def test_restock_sweet_admin_success(client):
    admin_headers = get_auth_header(client, email="admin@test.com", is_admin=True)
    sweet_id = create_sweet(client, admin_headers, quantity=10)
    
    response = client.post(f"/api/sweets/{sweet_id}/restock", json={
        "quantity_to_add": 50
    }, headers=admin_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Restock successful"
    assert data["sweet_id"] == sweet_id
    assert data["previous_quantity"] == 10
    assert data["new_quantity"] == 60
    assert data["quantity_added"] == 50


def test_restock_sweet_increases_stock(client):
    admin_headers = get_auth_header(client, email="admin@test.com", is_admin=True)
    sweet_id = create_sweet(client, admin_headers, quantity=5)
    
    # Restock 100
    client.post(f"/api/sweets/{sweet_id}/restock", json={
        "quantity_to_add": 100
    }, headers=admin_headers)
    
    # Check updated stock
    response = client.get("/api/sweets", headers=admin_headers)
    sweet = next(s for s in response.json() if s["sweet_id"] == sweet_id)
    assert sweet["quantity_in_stock"] == 105


def test_restock_sweet_non_admin_forbidden(client):
    # Create sweet as admin
    admin_headers = get_auth_header(client, email="admin@test.com", is_admin=True)
    sweet_id = create_sweet(client, admin_headers, quantity=10)
    
    # Try to restock as regular user
    user_headers = get_auth_header(client, email="user@test.com", is_admin=False)
    response = client.post(f"/api/sweets/{sweet_id}/restock", json={
        "quantity_to_add": 50
    }, headers=user_headers)
    
    assert response.status_code == 403


def test_restock_sweet_zero_quantity(client):
    admin_headers = get_auth_header(client, email="admin@test.com", is_admin=True)
    sweet_id = create_sweet(client, admin_headers, quantity=10)
    
    response = client.post(f"/api/sweets/{sweet_id}/restock", json={
        "quantity_to_add": 0
    }, headers=admin_headers)
    
    assert response.status_code == 422


def test_restock_sweet_negative_quantity(client):
    admin_headers = get_auth_header(client, email="admin@test.com", is_admin=True)
    sweet_id = create_sweet(client, admin_headers, quantity=10)
    
    response = client.post(f"/api/sweets/{sweet_id}/restock", json={
        "quantity_to_add": -20
    }, headers=admin_headers)
    
    assert response.status_code == 422


def test_restock_sweet_not_found(client):
    admin_headers = get_auth_header(client, email="admin@test.com", is_admin=True)
    
    response = client.post("/api/sweets/9999/restock", json={
        "quantity_to_add": 50
    }, headers=admin_headers)
    
    assert response.status_code == 404


def test_restock_sweet_requires_authentication(client):
    response = client.post("/api/sweets/1/restock", json={
        "quantity_to_add": 50
    })
    
    assert response.status_code == 401


def test_restock_out_of_stock_sweet(client):
    admin_headers = get_auth_header(client, email="admin@test.com", is_admin=True)
    sweet_id = create_sweet(client, admin_headers, quantity=0)
    
    response = client.post(f"/api/sweets/{sweet_id}/restock", json={
        "quantity_to_add": 100
    }, headers=admin_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["new_quantity"] == 100