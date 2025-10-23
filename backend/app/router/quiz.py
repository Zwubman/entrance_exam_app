from fastapi import APIRouter, Depends
from app.config.database import get_db

router = APIRouter(tags=['Quiz Routers'], prefix='/quizzes')

@router.post('/')
def generate_quiz():
    pass

@router.post('/submit')
def submit_quiz():
    pass

@router.post('/new-chat')
def create_new_chat_from_quiz():
    pass