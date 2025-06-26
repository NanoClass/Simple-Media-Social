from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None

class User(UserBase):
    id: int
    attributes: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    is_admin: bool = False

    class Config:
        from_attributes = True
