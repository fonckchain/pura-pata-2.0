from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime
import math

from ...core.database import get_db
from ...models.user import User
from ...models.dog import Dog
from ...models.status_history import DogStatusHistory
from ...schemas.dog import (
    DogCreate, DogUpdate, DogResponse, DogWithPublisher,
    DogStatusUpdate, DogSearchFilters
)
from .auth import get_current_user

router = APIRouter()


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in kilometers using Haversine formula"""
    R = 6371  # Earth's radius in kilometers

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


@router.get("/", response_model=List[DogWithPublisher])
async def get_dogs(
    db: Session = Depends(get_db),
    status_filter: Optional[str] = Query("disponible", description="Filter by status"),
    size: Optional[str] = Query(None, description="Filter by size"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    age_min: Optional[int] = Query(None, description="Minimum age in years"),
    age_max: Optional[int] = Query(None, description="Maximum age in years"),
    province: Optional[str] = Query(None, description="Filter by province"),
    latitude: Optional[float] = Query(None, description="User latitude for radius search"),
    longitude: Optional[float] = Query(None, description="User longitude for radius search"),
    radius_km: Optional[float] = Query(None, description="Search radius in kilometers"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Get all dogs with filters"""
    query = db.query(Dog)

    # Status filter
    if status_filter:
        query = query.filter(Dog.status == status_filter)

    # Size filter
    if size:
        query = query.filter(Dog.size == size)

    # Gender filter
    if gender:
        query = query.filter(Dog.gender == gender)

    # Age filter
    if age_min is not None:
        query = query.filter(Dog.age_years >= age_min)

    if age_max is not None:
        query = query.filter(Dog.age_years <= age_max)

    # Province filter
    if province:
        query = query.filter(Dog.province == province)

    # Get all dogs
    dogs = query.order_by(Dog.created_at.desc()).offset(skip).limit(limit).all()

    # Filter by radius if coordinates provided
    if latitude is not None and longitude is not None and radius_km is not None:
        filtered_dogs = []
        for dog in dogs:
            distance = calculate_distance(latitude, longitude, dog.latitude, dog.longitude)
            if distance <= radius_km:
                filtered_dogs.append(dog)
        dogs = filtered_dogs

    # Attach publisher info
    result = []
    for dog in dogs:
        dog_dict = DogResponse.model_validate(dog).model_dump()
        publisher = db.query(User).filter(User.id == dog.publisher_id).first()
        dog_dict['publisher'] = {
            'id': str(publisher.id),
            'name': publisher.name,
            'email': publisher.email
        } if publisher else None
        result.append(dog_dict)

    return result


@router.get("/{dog_id}", response_model=DogWithPublisher)
async def get_dog(
    dog_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific dog by ID"""
    dog = db.query(Dog).filter(Dog.id == dog_id).first()

    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dog not found"
        )

    # Attach publisher info
    dog_dict = DogResponse.model_validate(dog).model_dump()
    publisher = db.query(User).filter(User.id == dog.publisher_id).first()
    dog_dict['publisher'] = {
        'id': str(publisher.id),
        'name': publisher.name,
        'email': publisher.email,
        'phone': publisher.phone
    } if publisher else None

    return dog_dict


@router.post("/", response_model=DogResponse, status_code=status.HTTP_201_CREATED)
async def create_dog(
    dog_data: DogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new dog listing"""
    new_dog = Dog(
        **dog_data.model_dump(),
        publisher_id=current_user.id
    )

    db.add(new_dog)
    db.commit()
    db.refresh(new_dog)

    # Create initial status history
    status_history = DogStatusHistory(
        dog_id=new_dog.id,
        old_status=None,
        new_status='disponible'
    )
    db.add(status_history)
    db.commit()

    return new_dog


@router.put("/{dog_id}", response_model=DogResponse)
async def update_dog(
    dog_id: str,
    dog_data: DogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a dog listing"""
    dog = db.query(Dog).filter(Dog.id == dog_id).first()

    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dog not found"
        )

    # Check ownership
    if dog.publisher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this dog"
        )

    # Update fields
    update_data = dog_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(dog, field, value)

    db.commit()
    db.refresh(dog)

    return dog


@router.patch("/{dog_id}/status", response_model=DogResponse)
async def update_dog_status(
    dog_id: str,
    status_data: DogStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update dog status"""
    dog = db.query(Dog).filter(Dog.id == dog_id).first()

    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dog not found"
        )

    # Check ownership
    if dog.publisher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this dog"
        )

    # Prevent changing from 'adoptado' status
    if dog.status == 'adoptado':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change status of adopted dog"
        )

    old_status = dog.status
    dog.status = status_data.status

    # Set adopted_at timestamp
    if status_data.status == 'adoptado':
        dog.adopted_at = datetime.utcnow()

    # The trigger will automatically log the status change
    db.commit()
    db.refresh(dog)

    return dog


@router.delete("/{dog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dog(
    dog_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a dog listing"""
    dog = db.query(Dog).filter(Dog.id == dog_id).first()

    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dog not found"
        )

    # Check ownership
    if dog.publisher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this dog"
        )

    db.delete(dog)
    db.commit()

    return None


@router.get("/{dog_id}/history", response_model=List[dict])
async def get_dog_status_history(
    dog_id: str,
    db: Session = Depends(get_db)
):
    """Get status change history for a dog"""
    dog = db.query(Dog).filter(Dog.id == dog_id).first()

    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dog not found"
        )

    history = db.query(DogStatusHistory).filter(
        DogStatusHistory.dog_id == dog_id
    ).order_by(DogStatusHistory.changed_at.desc()).all()

    return [
        {
            'id': str(h.id),
            'old_status': h.old_status,
            'new_status': h.new_status,
            'changed_at': h.changed_at.isoformat()
        }
        for h in history
    ]
