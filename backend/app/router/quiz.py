from fastapi import APIRouter, Depends, UploadFile, File, Body
from app.config.database import get_db
from app.schema.exam import ExamSubmit, ExamChat
from app.router.chat import get_profile
from app.controller import exam, quiz

router = APIRouter(tags=['Quiz Routers'], prefix='/quizzes')

@router.post('/')
async def generate_quiz(query: str = Body(None), questions_length: int = Body(...), url: str | None = Body(None), file: UploadFile | str | None = File(None), db = Depends(get_db)):
    return await quiz.generate_quiz(query, questions_length, url, file, db)

@router.post('/submit')
def submit_quiz(req: ExamSubmit):
    return exam.submit_exam(req)

@router.post('/new-chat')
def create_new_chat_from_quiz(req: ExamChat, profile = Depends(get_profile), db = Depends(get_db)):
    return exam.create_new_chat_from_exam(req, profile, db)