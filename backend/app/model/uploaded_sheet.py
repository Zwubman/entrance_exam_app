from sqlalchemy import Column, Text
from app.config.database import Base
from .db_helper import DBHelper

class UploadedSheet(Base, DBHelper):
    __tablename__ = "uploaded_sheets"

    file_path = Column(
        Text,
        nullable=False,
    )