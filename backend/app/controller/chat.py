from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.model.chat import Chat
from app.model.profile import Profile
from app.model.conversation import Conversation
from app.schema.chat import ChatCreate, ChatConversation
from app.util.ai_helper.ai_chat_engine import ai_chat_engine
from app.util.ai_helper.short_summary import short_summary as ai_short_summary
from uuid import UUID

def create_new_chat(req: ChatCreate, profile: Profile, db: Session):
    if req.initial_idea:
        short_summary = ai_short_summary(req.initial_idea)

    new_chat = Chat(
        profile=profile,
        profile_id=profile.id,
        initial_idea=req.initial_idea or None,
        short_summary=short_summary or None
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat

def ask_ai(req: ChatConversation, chat_id: UUID, db: Session):
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.is_deleted == False
    ).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chat not found'
        )
    prev_conversations = db.query(Conversation).filter(
        Conversation.chat_id == chat_id,
        Conversation.is_deleted == False
    ).all()
    
    ai_answer = ai_chat_engine(req.user_question, chat, prev_conversations)
    new_conversation = Conversation(
        chat=chat,
        chat_id=chat.id,
        user_question=req.user_question,
        ai_answer=ai_answer
    )

    db.add(new_conversation)
    db.flush()
    db.commit()
    db.refresh(new_conversation)

    if not chat.short_summary:
        short_summary = ai_short_summary(req.user_question)
        chat.short_summary = short_summary
        db.commit()
        db.refresh(chat)

    return ai_answer

def get_chat_history(chat_id: UUID, db: Session):
    conversations = db.query(Conversation).filter(
        Conversation.chat_id == chat_id,
        Conversation.is_deleted == False
    ).all()
    return conversations

def list_all_chats(profile: Profile, db: Session):
    chats = db.query(Chat).filter(
        Chat.profile_id == Profile.id,
        Chat.is_deleted == False
    ).all()
    return chats

def delete_chat(chat_id: UUID, db: Session):
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.is_deleted == False
    ).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chat not found'
        )
    chat.soft_delete()
    db.commit()
    return "Deleted"