from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from ...models.user import User
from ...models.dog import Dog
from ...schemas.user import UserResponse, UserUpdate
from ...schemas.dog import DogResponse
from .auth import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update current user profile"""
    update_data = user_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user


@router.get("/me/dogs", response_model=List[DogResponse])
async def get_my_dogs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status_filter: str = None
):
    """Get all dogs published by current user"""
    query = db.query(Dog).filter(Dog.publisher_id == current_user.id)

    if status_filter:
        query = query.filter(Dog.status == status_filter)

    dogs = query.order_by(Dog.created_at.desc()).all()

    return dogs


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_profile(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get user profile by ID (public info only)"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.get("/{user_id}/dogs", response_model=List[DogResponse])
async def get_user_dogs(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get all available dogs published by a specific user"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Only show available dogs for other users
    dogs = db.query(Dog).filter(
        Dog.publisher_id == user_id,
        Dog.status == 'disponible'
    ).order_by(Dog.created_at.desc()).all()

    return dogs
