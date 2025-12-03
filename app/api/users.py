from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.user import UserResponse, UserUpdate, PasswordResetRequest
from app.models.user import User
from app.api.deps import get_current_user, get_current_admin_user
from app.core.security import get_password_hash

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        display_name=current_user.display_name,
        tagline=current_user.tagline,
        bio=current_user.bio,
        avatar_url=current_user.avatar_url,
        role=current_user.role,
        created_at=current_user.created_at
    )


@router.patch("/me", response_model=UserResponse)
def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_update.display_name is not None:
        current_user.display_name = user_update.display_name
    if user_update.tagline is not None:
        current_user.tagline = user_update.tagline
    if user_update.bio is not None:
        current_user.bio = user_update.bio
    if user_update.avatar_url is not None:
        current_user.avatar_url = user_update.avatar_url
    
    db.commit()
    db.refresh(current_user)
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        display_name=current_user.display_name,
        tagline=current_user.tagline,
        bio=current_user.bio,
        avatar_url=current_user.avatar_url,
        role=current_user.role,
        created_at=current_user.created_at
    )


@router.get("/", response_model=List[UserResponse])
def get_all_users(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return [
        UserResponse(
            id=str(user.id),
            email=user.email,
            display_name=user.display_name,
            tagline=user.tagline,
            bio=user.bio,
            avatar_url=user.avatar_url,
            role=user.role,
            created_at=user.created_at
        )
        for user in users
    ]


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(
        id=str(user.id),
        email=user.email,
        display_name=user.display_name,
        tagline=user.tagline,
        bio=user.bio,
        avatar_url=user.avatar_url,
        role=user.role,
        created_at=user.created_at
    )


@router.post("/{user_id}/reset-password", response_model=dict)
def reset_user_password(
    user_id: str,
    password_reset: PasswordResetRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Admin can reset any user's password"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update password
    user.hashed_password = get_password_hash(password_reset.new_password)
    db.commit()
    
    return {"message": f"Password reset successfully for user {user.email}"}
