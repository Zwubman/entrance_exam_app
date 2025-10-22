from sqlalchemy import Boolean, Column, Uuid, String, DateTime, Enum, func
from app.config.database import Base
import uuid

class User(Base):
    __tablename__ = 'users'

    id = Column(
        Uuid,
        primary_key=True,
        index=True,
        default=uuid.uuid1
    )
    username = Column(
        String(255),
        nullable=False,
    )
    email = Column(
        String(255),
        nullable=False,
        unique=True
    )
    password = Column(
        String(255),
        nullable=False
    )
    role = Column(
        Enum(
            'Admin',
            'Student',
        ),
        nullable=False,
        default='Student'
    )
    grade = Column(
        Enum(
            'Grade - 9',
            'Grade - 10',
            'Grade - 11',           
            'Grade - 12',
            'Freshman'
        )
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