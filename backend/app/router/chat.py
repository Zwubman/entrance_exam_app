from fastapi import APIRouter, Depends
from app.config.database import get_db

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
def list_all_chats():
    pass

@router.delete('/{chat_id}')
def delete_chat():
    pass