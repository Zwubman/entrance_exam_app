from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base
from .db_helper import DBHelper

class Chat(Base, DBHelper):
    __tablename__ = 'chats'

    short_summary = Column(
        String(255),
        nullable=True,
        comment="Brief summary of the chat conversation"
    )

    profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey('profiles.id'),
        nullable=False,
        index=True,
        comment="Reference to the profile that owns this chat"
    )

    profile = relationship('Profile', back_populates='chats')
    conversations = relationship('Conversation', back_populates='chat', cascade="all, delete-orphan")