"""
Authentication routes for user registration and login.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import UserAccount
from app.schemas import (
    UserRegistrationRequest,
    UserLoginRequest,
    UserProfileResponse,
    AuthenticationToken
)
from app.auth.password_hasher import hash_password
from app.auth.token_manager import create_access_token
from app.auth.authentication_service import authenticate_user, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    registration_data: UserRegistrationRequest,
    db: Session = Depends(get_db)
):
    """Register a new user account."""
    # Check if email already exists
    existing_user = db.query(UserAccount).filter(
        UserAccount.email_address == registration_data.email_address
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email address already registered"
        )
    
    # Create new user
    new_user = UserAccount(
        email_address=registration_data.email_address,
        full_name=registration_data.full_name,
        hashed_password=hash_password(registration_data.password),
        is_administrator=registration_data.is_administrator
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email address already registered"
        )
    
    return new_user



@router.post("/login", response_model=AuthenticationToken)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate user and return access token - OAuth2 compatible."""
    # OAuth2 spec uses 'username' field for email
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.user_id)})  # Note: string
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserProfileResponse)
def get_current_user_profile(current_user: UserAccount = Depends(get_current_user)):
    """Get current authenticated user's profile."""
    return current_user