from sqlalchemy import Boolean, Column, Uuid, String, DateTime, Enum, func
from app.config.database import Base
import uuid

class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(
        Uuid,
        primary_key=True,
        index=True,
        default=uuid.uuid1
    )
    device_id = Column(
        String(255),
        nullable=False,
        unique=True
    )
    category = Column(
        Enum(
            'Freshman',
            'Entrance',
            'Exit'
        ),
        default='Entrance',
        nullable=False
    )
    is_deleted = Column(
        Boolean,
        default=False
    )
    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False
    )