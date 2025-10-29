from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from app.config.database import Base
from .db_helper import DBHelper

class Profile(Base, DBHelper):
    __tablename__ = 'profiles'

    device_id = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        comment="Unique device identifier"
    )
    
    category = Column(
        Enum(
            'Freshman',
            'Entrance',
            name='profile_category'
        ),
        default='Entrance',
        nullable=False,
        comment="Profile category type"
    )
    
    stream = Column(
        Enum(
            'Natural',
            'Social',
            'Both',
            name='profile_stream'
        ),
        nullable=True,
        comment="Academic stream"
    )

    chats = relationship('Chat', back_populates='profile', cascade="all, delete-orphan")