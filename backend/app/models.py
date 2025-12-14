"""
Database models - User only for now.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
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


class SweetProduct(DatabaseBaseModel):
    """Represents a sweet product available in the shop."""
    __tablename__ = "sweet_products"

    sweet_id = Column(Integer, primary_key=True, index=True)
    sweet_name = Column(String, nullable=False, index=True)
    sweet_category = Column(String, nullable=False, index=True)
    sweet_price = Column(Float, nullable=False)
    quantity_in_stock = Column(Integer, nullable=False, default=0)
    sweet_description = Column(String, nullable=True)
    product_created_at = Column(DateTime(timezone=True), server_default=func.now())
    product_updated_at = Column(DateTime(timezone=True), onupdate=func.now())