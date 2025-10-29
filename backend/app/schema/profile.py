from pydantic import BaseModel
from typing import Optional

class ProfileCreate(BaseModel):
    device_id: str
    category: Optional[str] = "Entrance"  # default value
    stream: Optional[str] = None


class ProfileUpdate(BaseModel):
    device_id: Optional[str] = None
    category: Optional[str] = None
    stream: Optional[str] = None

class ProfileResponse(BaseModel):
    id: str
    device_id: str
    category: str
    stream: Optional[str] = None

    model_config = {
        "from_attributes": True  # <-- use this instead of orm_mode
    }