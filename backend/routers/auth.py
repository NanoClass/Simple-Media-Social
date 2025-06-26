from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated
from sqlalchemy.orm import Session

from models.base import User
from database import get_db
from schemas.auth import Token
from services.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash
)

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    # Check if user already exists
    existing_user = db.query(User).filter(
        User.username == form_data.username
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Create new user (inactive by default)
    user = User(
        username=form_data.username,
        email=form_data.email if hasattr(form_data, 'email') else f"{form_data.username}@example.com",
        password_hash=get_password_hash(form_data.password),
        is_active=False,  # Requires admin approval
        attributes={}
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
