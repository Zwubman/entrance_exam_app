from sqlalchemy import Column, String, Uuid, ForeignKey, Text
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

    initial_idea = Column(
        Text,
        nullable=True
    )

    profile_id = Column(
        Uuid,
        ForeignKey('profiles.id'),
        nullable=False,
        index=True,
        comment="Reference to the profile that owns this chat"
    )

    profile = relationship('Profile', back_populates='chats')
    conversations = relationship('Conversation', back_populates='chat', cascade="all, delete-orphan")