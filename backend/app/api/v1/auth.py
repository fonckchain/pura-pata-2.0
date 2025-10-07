from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional

from ...core.database import get_db
from ...core.config import settings
from ...core.security import create_access_token, verify_token
from ...models.user import User
from ...schemas.auth import Token
from ...schemas.user import UserCreate, UserResponse

router = APIRouter()
security = HTTPBearer()


def get_supabase_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify Supabase JWT token and extract user info"""
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    return payload


async def get_current_user(
    db: Session = Depends(get_db),
    token_data: dict = Depends(get_supabase_user)
) -> User:
    """Get current user from database"""
    user_id = token_data.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user in our database.
    Note: Supabase Auth handles the actual authentication.
    This endpoint creates the user profile in our database.
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Create new user
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        phone=user_data.phone,
        location=user_data.location
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile"""
    return current_user


@router.post("/sync", response_model=UserResponse)
async def sync_user_from_supabase(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(get_supabase_user)
):
    """
    Sync user from Supabase Auth to our database.
    Called after successful Supabase authentication.
    """
    user_id = token_data.get("sub")

    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        # Update existing user
        user.name = user_data.name
        user.phone = user_data.phone
        user.location = user_data.location
    else:
        # Create new user with Supabase ID
        user = User(
            id=user_id,
            email=user_data.email,
            name=user_data.name,
            phone=user_data.phone,
            location=user_data.location
        )
        db.add(user)

    db.commit()
    db.refresh(user)

    return user
