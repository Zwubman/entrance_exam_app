from fastapi import APIRouter, Depends
from app.schema.user import UserCreate, UserLogin
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.controller import user
from app.util.token import auth_checker

router = APIRouter(tags=['Chat Routers'], prefix='/chats')

@router.post('/new')
def create_new_chat():
    pass

@router.post('/{chat_id}/ask')
def ask_ai():
    pass

@router.get('/{chat_id}/history')
def get_chat_history():
    pass

@router.get('/')
def list_chats():
    pass