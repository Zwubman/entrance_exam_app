from sqlalchemy import Column, Text, Uuid, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base
from .db_helper import DBHelper

class Conversation(Base, DBHelper):
    __tablename__ = 'conversations'

    user_question = Column(
        Text,
        nullable=False,
        comment="User's question or input"
    )

    ai_answer = Column(
        Text,
        nullable=True,
        comment="AI's answer to the user input"
    )

    chat_id = Column(
        Uuid,
        ForeignKey('chats.id'),
        nullable=False,
        index=True,
        comment="Reference to the parent chat"
    )
    
    chat = relationship('Chat', back_populates='conversations')