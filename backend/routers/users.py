from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from models.base import User
from database import get_db
from schemas.users import User as UserSchema

router = APIRouter()

@router.get("/id/{user_id}", response_model=UserSchema)
async def get_user_by_id(
    user_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/username/{username}", response_model=UserSchema)
async def get_user_by_username(
    username: str,
    db: Annotated[Session, Depends(get_db)]
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
