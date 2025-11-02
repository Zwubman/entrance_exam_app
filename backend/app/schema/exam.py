from pydantic import BaseModel
from typing import Optional, Any

class ExamInsert(BaseModel):
    year: str
    subject: str
    extra_data: Optional[str] = None

class ExamSearch(BaseModel):
    query: Optional[str] = None
    year: Optional[str] = None
    subject: Optional[str] = None
    extra_data: Optional[str] = None
    next_page: Optional[int] = 0
    questions_length: int = 10

class ExamSubmit(BaseModel):
    questions: Any
    answers: Any

class ExamChat(BaseModel):
    questions: Any
    answers: Any
    evaluations: Optional[Any] = None