from sqlalchemy import Column, Text, Integer
from app.config.database import Base
from .db_helper import DBHelper

class Feedback(Base, DBHelper):
    __tablename__ = "feedbacks"

    comment = Column(
        Text,
        nullable=False,
    )

    rate = Column(
        Integer,
        nullable=False,
    )