from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from OVPMS.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Google identity
    google_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    # Profile info
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True)

    # Authorization
    role = Column(String, default="user", nullable=False)

    # Status
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)