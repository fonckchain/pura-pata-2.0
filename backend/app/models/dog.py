from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..core.database import Base


class Dog(Base):
    __tablename__ = "dogs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Basic info
    name = Column(String(100), nullable=False)
    age_years = Column(Integer, nullable=False)
    age_months = Column(Integer, default=0)
    breed = Column(String(100), nullable=False)
    size = Column(String(20), nullable=False)  # pequeño, mediano, grande
    gender = Column(String(10), nullable=False)  # macho, hembra
    color = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    # Health info
    vaccinated = Column(Boolean, default=False)
    sterilized = Column(Boolean, default=False)
    dewormed = Column(Boolean, default=False)
    special_needs = Column(Text, nullable=True)

    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(Text, nullable=True)
    province = Column(String(50), nullable=True)

    # Contact
    contact_phone = Column(String(20), nullable=False)
    contact_email = Column(String(255), nullable=True)

    # Media
    photos = Column(ARRAY(Text), nullable=False)
    certificate = Column(Text, nullable=True)

    # Status
    status = Column(String(20), default='disponible', nullable=False)

    # Relations
    publisher_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    adopted_at = Column(DateTime, nullable=True)

    # Relationships
    publisher = relationship("User", back_populates="dogs")
    status_history = relationship("DogStatusHistory", back_populates="dog", cascade="all, delete-orphan")

    # Constraints
    __table_args__ = (
        CheckConstraint("status IN ('disponible', 'reservado', 'adoptado')", name='valid_status'),
        Index('idx_dogs_status', 'status'),
        Index('idx_dogs_publisher', 'publisher_id'),
    )
