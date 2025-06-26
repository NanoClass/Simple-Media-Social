from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.base import Like, Share, Follow, Post, User
from schemas.posts import PostSchema
from database import get_db
from services.auth import get_current_user
from schemas.posts import PostCreate

router = APIRouter()

@router.post("/{post_id}/reply", response_model=PostSchema)
async def reply_to_post(
    post_id: int,
    post_data: PostCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    # Validate parent post exists
    parent_post = db.query(Post).filter(Post.id == post_id).first()
    if not parent_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent post not found"
        )

    # Validate post content
    from services.validation import validate_post
    cleaned_content, is_valid = validate_post(post_data.content)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post content is not valid"
        )

    # Create reply
    reply = Post(
        user_id=current_user.id,
        content=cleaned_content,
        parent_id=post_id,
        is_validated=True
    )
    db.add(reply)
    
    # Update parent post counts and timestamps
    parent_post = db.query(Post).filter(Post.id == post_id).first()
    parent_post.replies_count += 1
    parent_post.updated_at = func.now()
    
    db.commit()
    db.refresh(reply)
    return reply

@router.post("/{post_id}/like")
async def like_post(
    post_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    # Check if like already exists
    existing_like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.post_id == post_id
    ).first()
    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post already liked"
        )

    like = Like(user_id=current_user.id, post_id=post_id)
    db.add(like)
    
    # Update post counts and timestamps
    post = db.query(Post).filter(Post.id == post_id).first()
    post.likes_count += 1
    post.updated_at = func.now()
    
    db.commit()
    return {"message": "Post liked successfully"}

@router.post("/{post_id}/share")
async def share_post(
    post_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    share = Share(user_id=current_user.id, post_id=post_id)
    db.add(share)
    
    # Update post counts and timestamps
    post = db.query(Post).filter(Post.id == post_id).first()
    post.shares_count += 1
    post.updated_at = func.now()
    
    db.commit()
    return {"message": "Post shared successfully"}

@router.post("/{user_id}/follow")
async def follow_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    # Check if trying to follow self
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot follow yourself"
        )

    # Check if follow already exists
    existing_follow = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == user_id
    ).first()
    if existing_follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already following this user"
        )

    follow = Follow(follower_id=current_user.id, following_id=user_id)
    db.add(follow)
    db.commit()
    return {"message": "User followed successfully"}
