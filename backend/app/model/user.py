from sqlalchemy import Column, String, Enum
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

    password = Column(
        String(255),
        nullable=False,
        comment="Hashed password"
    )

    role = Column(
        Enum(
            'super_admin',
            'admin',
            name='role_type'
        ),
        nullable=False,
        default='admin'
    )