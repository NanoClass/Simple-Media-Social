from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.base import Post, User
from schemas.posts import PostUpdate
from services.auth import get_current_user
from database import get_db
from schemas.posts import PostCreate, PostSchema, PaginatedPosts
from services.validation import validate_post
from services.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=PostSchema)
async def create_post(
    post: PostCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    # Validate post content
    cleaned_content, is_valid = validate_post(post.content)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post content is not valid"
        )

    # Create post
    db_post = Post(
        user_id=current_user.id,
        content=cleaned_content,
        is_validated=is_valid
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.patch("/{post_id}", response_model=PostSchema)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own posts"
        )

    if post_update.content is not None:
        # Validate new content
        from services.validation import validate_post
        cleaned_content, is_valid = validate_post(post_update.content)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Post content is not valid"
            )
        post.content = cleaned_content
        post.modified_at = func.now()

    post.updated_at = func.now()
    db.commit()
    db.refresh(post)
    return post

@router.get("/{post_id}", response_model=PostSchema)
async def get_post(
    post_id: int,
    db: Annotated[Session, Depends(get_db)],
    replies_page: int = 1,
    replies_per_page: int = 5
):
    # Get main post
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Get paginated replies
    offset = (replies_page - 1) * replies_per_page
    replies = db.query(Post).filter(Post.parent_id == post_id)\
               .order_by(Post.created_at.desc())\
               .offset(offset).limit(replies_per_page).all()

    # Convert to dict and add replies
    post_dict = post.__dict__
    post_dict.update({
        'replies': replies
    })

    return post_dict

@router.get("/user/id/{user_id}", response_model=PaginatedPosts)
async def get_posts_by_user_id(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    per_page: int = 10
):
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must be greater than 0"
        )
    if per_page < 1 or per_page > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Per page must be between 1 and 100"
        )

    offset = (page - 1) * per_page
    posts = db.query(Post).filter(Post.user_id == user_id)
    total = posts.count()
    posts = posts.offset(offset).limit(per_page).all()
    
    return PaginatedPosts(
        posts=posts,
        total=total,
        page=page,
        per_page=per_page
    )

@router.get("/user/username/{username}", response_model=PaginatedPosts)
async def get_posts_by_username(
    username: str,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    per_page: int = 10
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return await get_posts_by_user_id(user.id, db, page, per_page)
