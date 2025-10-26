from pydantic import BaseModel
from typing import Optional

class ChatCreate(BaseModel):
    initial_idea: Optional[str] = None

class ChatConversation(BaseModel):
    user_question: str