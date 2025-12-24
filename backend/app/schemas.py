"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime


# ==================== Authentication Schemas ====================

class UserRegistrationRequest(BaseModel):
    """Schema for new user registration."""
    email_address: EmailStr
    full_name: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=100)
    is_administrator: bool = False

    @field_validator('full_name')
    @classmethod
    def validate_full_name_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('Full name cannot be empty or just whitespace')
        return value.strip()


class UserLoginRequest(BaseModel):
    """Schema for user login."""
    username: EmailStr
    password: str


class AuthenticationToken(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class UserProfileResponse(BaseModel):
    """Schema for user profile data returned to client."""
    user_id: int
    email_address: str
    full_name: str
    is_administrator: bool
    account_created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== Sweet Product Schemas ====================

class SweetCreationRequest(BaseModel):
    """Schema for creating a new sweet product."""
    sweet_name: str = Field(min_length=1, max_length=200)
    sweet_category: str = Field(min_length=1, max_length=100)
    sweet_price: float = Field(gt=0, description="Price must be greater than 0")
    quantity_in_stock: int = Field(ge=0, description="Quantity cannot be negative")
    sweet_description: Optional[str] = Field(None, max_length=500)

    @field_validator('sweet_name', 'sweet_category')
    @classmethod
    def validate_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('Field cannot be empty or just whitespace')
        return value.strip()


class SweetUpdateRequest(BaseModel):
    """Schema for updating an existing sweet product."""
    sweet_name: Optional[str] = Field(None, min_length=1, max_length=200)
    sweet_category: Optional[str] = Field(None, min_length=1, max_length=100)
    sweet_price: Optional[float] = Field(None, gt=0)
    quantity_in_stock: Optional[int] = Field(None, ge=0)
    sweet_description: Optional[str] = Field(None, max_length=500)


class SweetProductResponse(BaseModel):
    """Schema for sweet product data returned to client."""
    sweet_id: int
    sweet_name: str
    sweet_category: str
    sweet_price: float
    quantity_in_stock: int
    sweet_description: Optional[str]
    product_created_at: datetime
    product_updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


# ==================== Inventory Management Schemas ====================

class PurchaseRequest(BaseModel):
    """Schema for purchasing sweets."""
    quantity_to_purchase: int = Field(gt=0, description="Must purchase at least 1 item")
    coupon: Optional[str]


class RestockRequest(BaseModel):
    """Schema for restocking sweets."""
    quantity_to_add: int = Field(gt=0, description="Must restock at least 1 item")


class InventoryOperationResponse(BaseModel):
    """Schema for inventory operation results."""
    message: str
    sweet_id: int
    sweet_name: str
    previous_quantity: int
    new_quantity: int
    total_price: Optional[float]
    discounted_price: Optional[float]
    quantity_purchased: Optional[int] = None
    quantity_added: Optional[int] = None