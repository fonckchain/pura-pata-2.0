from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..core.database import Base


class DogStatusHistory(Base):
    __tablename__ = "dog_status_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dog_id = Column(UUID(as_uuid=True), ForeignKey('dogs.id', ondelete='CASCADE'), nullable=False)
    old_status = Column(String(20), nullable=True)
    new_status = Column(String(20), nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    dog = relationship("Dog", back_populates="status_history")
