"""
Authentication service handling user verification.
"""
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.database import get_db
from app.models import UserAccount
from app.auth.password_hasher import verify_password
from app.auth.token_manager import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def authenticate_user(db: Session, email: str, password: str) -> Optional[UserAccount]:
    """Verify user credentials and return user if valid."""
    user = db.query(UserAccount).filter(UserAccount.email_address == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserAccount:
    """Dependency to get current authenticated user from token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")  # ← CHANGE: str not int
    if user_id is None:
        raise credentials_exception
    
    user = db.query(UserAccount).filter(UserAccount.user_id == int(user_id)).first()  # ← Convert to int
    if user is None:
        raise credentials_exception
    
    return user

def require_admin(current_user: UserAccount = Depends(get_current_user)) -> UserAccount:
    """Dependency to require admin privileges."""
    if not current_user.is_administrator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required"
        )
    return current_user