from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Literal
from datetime import datetime
from uuid import UUID


class DogBase(BaseModel):
    name: str
    age_years: int
    age_months: int = 0
    breed: str
    size: Literal['pequeño', 'mediano', 'grande']
    gender: Literal['macho', 'hembra']
    color: str
    description: Optional[str] = None

    vaccinated: bool = False
    sterilized: bool = False
    dewormed: bool = False
    special_needs: Optional[str] = None

    latitude: float
    longitude: float
    address: Optional[str] = None
    province: Optional[str] = None

    contact_phone: str
    contact_email: Optional[EmailStr] = None


class DogCreate(DogBase):
    photos: List[str]  # URLs after upload
    certificate: Optional[str] = None

    @field_validator('photos')
    @classmethod
    def validate_photos(cls, v):
        if not v or len(v) == 0:
            raise ValueError('At least one photo is required')
        if len(v) > 5:
            raise ValueError('Maximum 5 photos allowed')
        return v


class DogUpdate(BaseModel):
    name: Optional[str] = None
    age_years: Optional[int] = None
    age_months: Optional[int] = None
    breed: Optional[str] = None
    size: Optional[Literal['pequeño', 'mediano', 'grande']] = None
    gender: Optional[Literal['macho', 'hembra']] = None
    color: Optional[str] = None
    description: Optional[str] = None

    vaccinated: Optional[bool] = None
    sterilized: Optional[bool] = None
    dewormed: Optional[bool] = None
    special_needs: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    province: Optional[str] = None

    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None

    photos: Optional[List[str]] = None
    certificate: Optional[str] = None


class DogStatusUpdate(BaseModel):
    status: Literal['disponible', 'reservado', 'adoptado']


class DogResponse(DogBase):
    id: UUID
    photos: List[str]
    certificate: Optional[str] = None
    status: str
    publisher_id: UUID
    created_at: datetime
    updated_at: datetime
    adopted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DogWithPublisher(DogResponse):
    publisher: Optional[dict] = None


class DogSearchFilters(BaseModel):
    size: Optional[Literal['pequeño', 'mediano', 'grande']] = None
    gender: Optional[Literal['macho', 'hembra']] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    province: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_km: Optional[float] = None
    status: Optional[Literal['disponible', 'reservado', 'adoptado']] = 'disponible'
