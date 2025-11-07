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