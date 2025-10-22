from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    grade: Optional[str]


class UserLogin(BaseModel):
    email: EmailStr
    password: str