from fastapi import APIRouter, Depends, Header, HTTPException, status
from app.config.database import get_db
from app.controller import chat
from app.schema.chat import ChatCreate, ChatConversation
from app.model.profile import Profile
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter(tags=['Chat Routers'], prefix='/chats')

def get_profile(device_id: str = Header(...), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(
        Profile.device_id == device_id, 
        Profile.is_deleted == False
    ).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Profile not found for this device ID'
        )
    return profile

@router.post('/new')
def create_new_chat(req: ChatCreate, profile = Depends(get_profile), db = Depends(get_db)):
    return chat.create_new_chat(req, profile, db)

@router.post('/{chat_id}/ask')
def ask_ai(req: ChatConversation, chat_id, db = Depends(get_db)):
    return chat.ask_ai(req, UUID(chat_id), db)

@router.get('/{chat_id}/history')
def get_chat_history(chat_id, db = Depends(get_db)):
    return chat.get_chat_history(UUID(chat_id), db)

@router.get('/')
def list_all_chats(profile = Depends(get_profile), db = Depends(get_db)):
    return chat.list_all_chats(profile, db)

@router.delete('/{chat_id}')
def delete_chat(chat_id, db = Depends(get_db)):
    return chat.delete_chat(UUID(chat_id), db)
