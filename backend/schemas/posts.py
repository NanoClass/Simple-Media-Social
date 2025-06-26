from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    pass

class PostSchema(PostBase):
    id: int
    user_id: int
    is_validated: bool
    created_at: datetime
    updated_at: datetime
    modified_at: Optional[datetime] = None
    parent_id: Optional[int] = None
    replies_count: int = 0
    likes_count: int = 0
    shares_count: int = 0
    replies: List["PostSchema"] = []

    class Config:
        from_attributes = True

class PostUpdate(BaseModel):
    content: Optional[str] = None

class PaginatedPosts(BaseModel):
    posts: List[PostSchema]
    total: int
    page: int
    per_page: int = Field(10, ge=1, le=100)
