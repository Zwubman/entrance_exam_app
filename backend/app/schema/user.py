from pydantic import BaseModel, EmailStr
from typing import Optional

class AddAdmin(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "admin"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    role: str

    model_config = {
        "from_attributes": True  # <-- use this instead of orm_mode
    }


class DeleteResponse(BaseModel):
    success: bool
    message: str
