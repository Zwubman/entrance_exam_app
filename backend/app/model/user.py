from sqlalchemy import Column, String
from app.config.database import Base
from .db_helper import DBHelper

class User(Base, DBHelper):
    __tablename__ = "users"

    email = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        comment="User email address"
    )

    hashed_password = Column(
        String(255),
        nullable=False,
        comment="Hashed password"
    )