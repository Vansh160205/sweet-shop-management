"""
Pydantic schemas - Auth only for now.
"""
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
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
    email_address: EmailStr
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