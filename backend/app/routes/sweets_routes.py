"""
Sweet product routes for CRUD operations.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SweetProduct, UserAccount
from app.schemas import (
    SweetCreationRequest,
    SweetUpdateRequest,
    SweetProductResponse
)
from app.auth.authentication_service import get_current_user, require_admin

router = APIRouter(prefix="/api/sweets", tags=["Sweets"])


@router.post("", response_model=SweetProductResponse, status_code=status.HTTP_201_CREATED)
def create_sweet(
    sweet_data: SweetCreationRequest,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_admin)
):
    """Create a new sweet product."""
    new_sweet = SweetProduct(
        sweet_name=sweet_data.sweet_name,
        sweet_category=sweet_data.sweet_category,
        sweet_price=sweet_data.sweet_price,
        quantity_in_stock=sweet_data.quantity_in_stock,
        sweet_description=sweet_data.sweet_description
    )
    
    db.add(new_sweet)
    db.commit()
    db.refresh(new_sweet)
    
    return new_sweet


@router.get("", response_model=List[SweetProductResponse])
def get_all_sweets(
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    """Get all sweet products."""
    sweets = db.query(SweetProduct).all()
    return sweets


@router.get("/search", response_model=List[SweetProductResponse])
def search_sweets(
    name: Optional[str] = Query(None, description="Search by sweet name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    """Search sweets by name, category, or price range."""
    query = db.query(SweetProduct)
    
    if name:
        query = query.filter(SweetProduct.sweet_name.ilike(f"%{name}%"))
    
    if category:
        query = query.filter(SweetProduct.sweet_category.ilike(f"%{category}%"))
    
    if min_price is not None:
        query = query.filter(SweetProduct.sweet_price >= min_price)
    
    if max_price is not None:
        query = query.filter(SweetProduct.sweet_price <= max_price)
    
    return query.all()


@router.put("/{sweet_id}", response_model=SweetProductResponse)
def update_sweet(
    sweet_id: int,
    sweet_data: SweetUpdateRequest,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_admin)
):
    """Update an existing sweet product."""
    sweet = db.query(SweetProduct).filter(SweetProduct.sweet_id == sweet_id).first()
    
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    # Update only provided fields
    update_data = sweet_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sweet, field, value)
    
    db.commit()
    db.refresh(sweet)
    
    return sweet


@router.delete("/{sweet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_admin)  # Admin only!
):
    """Delete a sweet product (Admin only)."""
    sweet = db.query(SweetProduct).filter(SweetProduct.sweet_id == sweet_id).first()
    
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    db.delete(sweet)
    db.commit()
    
    return None