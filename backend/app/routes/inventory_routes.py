"""
Inventory management routes for purchase and restock operations.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SweetProduct, UserAccount
from app.schemas import (
    PurchaseRequest,
    RestockRequest,
    InventoryOperationResponse
)
from app.auth.authentication_service import get_current_user, require_admin

router = APIRouter(prefix="/api/sweets", tags=["Inventory"])


@router.post("/{sweet_id}/purchase", response_model=InventoryOperationResponse)
def purchase_sweet(
    sweet_id: int,
    purchase_data: PurchaseRequest,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    """Purchase a sweet, decreasing its quantity."""
    sweet = db.query(SweetProduct).filter(SweetProduct.sweet_id == sweet_id).first()
    
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    # Check if enough stock available
    if sweet.quantity_in_stock < purchase_data.quantity_to_purchase:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Only {sweet.quantity_in_stock} items available."
        )
    
    # Store previous quantity
    previous_quantity = sweet.quantity_in_stock
    
    # Decrease stock
    sweet.quantity_in_stock -= purchase_data.quantity_to_purchase
    
    total_price = float(sweet.sweet_price * purchase_data.quantity_to_purchase).__round__(2)

    discounted_price=0
    if(purchase_data.coupon=='COUPON'):
        discounted_price= float(0.9 * total_price).__round__(2)

    db.commit()
    db.refresh(sweet)
    
    return {
        "message": "Purchase successful",
        "sweet_id": sweet.sweet_id,
        "sweet_name": sweet.sweet_name,
        "previous_quantity": previous_quantity,
        "new_quantity": sweet.quantity_in_stock,
        "quantity_purchased": purchase_data.quantity_to_purchase,
        "total_price":total_price,
        "discounted_price":discounted_price
    }


@router.post("/{sweet_id}/restock", response_model=InventoryOperationResponse)
def restock_sweet(
    sweet_id: int,
    restock_data: RestockRequest,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_admin)  # Admin only!
):
    """Restock a sweet, increasing its quantity (Admin only)."""
    sweet = db.query(SweetProduct).filter(SweetProduct.sweet_id == sweet_id).first()
    
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    # Store previous quantity
    previous_quantity = sweet.quantity_in_stock
    
    # Increase stock
    sweet.quantity_in_stock += restock_data.quantity_to_add
    
    db.commit()
    db.refresh(sweet)
    
    return {
        "message": "Restock successful",
        "sweet_id": sweet.sweet_id,
        "sweet_name": sweet.sweet_name,
        "previous_quantity": previous_quantity,
        "new_quantity": sweet.quantity_in_stock,
        "quantity_added": restock_data.quantity_to_add
    }