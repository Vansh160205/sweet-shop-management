"""
Database models - User only for now.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import DatabaseBaseModel


class UserAccount(DatabaseBaseModel):
    """Represents a user account in the system."""
    __tablename__ = "user_accounts"

    user_id = Column(Integer, primary_key=True, index=True)
    email_address = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_administrator = Column(Boolean, default=False)
    account_created_at = Column(DateTime(timezone=True), server_default=func.now())
    account_updated_at = Column(DateTime(timezone=True), onupdate=func.now())