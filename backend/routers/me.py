from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel

from models.base import User
from database import get_db
from schemas.users import User as UserSchema
from services.auth import get_current_user, get_password_hash, verify_password

router = APIRouter()

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

@router.get("/", response_model=UserSchema)
async def get_current_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user

@router.patch("/attributes")
async def update_user_attributes(
    attributes: dict,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    current_user.attributes = attributes
    db.commit()
    db.refresh(current_user)
    return {"message": "Attributes updated successfully"}

@router.post("/change-password")
async def change_password(
    password_data: ChangePasswordRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    # Verify current password
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Update password
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}
