from sqlalchemy import Column, Text
from app.config.database import Base, SessionLocal
from langchain_core.caches import BaseCache
from .db_helper import DBHelper
from typing import Optional

class AICache(Base, DBHelper):
    __tablename__ = "ai_caches"

    prompt = Column(
        Text,
        nullable=False
    )

    llm_string = Column(
        Text,
        nullable=False
    )

    response = Column(
        Text,
        nullable=False
    )

class SQLAlchemyCache(BaseCache):
    def __init__(self, db_session_factory=SessionLocal):
        self.db_session_factory = db_session_factory

    def lookup(self, prompt: str, llm_string: str) -> Optional[str]:
        with self.db_session_factory() as session:
            entry = (
                session.query(AICache)
                .filter_by(prompt=prompt, llm_string=llm_string)
                .first()
            )
            return entry.response if entry else None

    def update(self, prompt: str, llm_string: str, return_val: str) -> None:
        with self.db_session_factory() as session:
            entry = (
                session.query(AICache)
                .filter_by(prompt=prompt, llm_string=llm_string)
                .first()
            )
            if entry:
                entry.response = return_val
            else:
                entry = AICache(prompt=prompt, llm_string=llm_string, response=return_val)
                session.add(entry)
            session.commit()

    def clear(self, *args, **kwargs) -> None:
        with self.db_session_factory() as session:
            session.query(AICache).delete()
            session.commit()