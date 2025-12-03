from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse
from app.api.deps import get_current_user
from pydantic import BaseModel

router = APIRouter()


class UpdateUserRoleRequest(BaseModel):
    role: UserRole


def require_admin(current_user: User = Depends(get_current_user)):
    """Dependency to require admin role"""
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this endpoint"
        )
    return current_user


@router.get("/users", response_model=List[UserResponse])
def list_all_users(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get all users - accessible by admin only"""
    users = db.query(User).all()
    
    # Convert UUIDs to strings
    return [
        UserResponse(
            id=str(user.id),
            email=user.email,
            display_name=user.display_name,
            tagline=user.tagline,
            bio=user.bio,
            avatar_url=user.avatar_url,
            role=user.role,
            is_protected=user.is_protected,
            created_at=user.created_at
        )
        for user in users
    ]


@router.patch("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: str,
    role_update: UpdateUserRoleRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update a user's role - accessible by admin only"""
    
    # Early validation: prevent admin from demoting themselves (no DB lock needed)
    if str(user_id) == str(current_user.id) and role_update.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot demote yourself. Ask another admin to change your role."
        )
    
    try:
        # Find user with row-level lock (SELECT FOR UPDATE)
        user = db.query(User).filter(User.id == user_id).with_for_update().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # PROTECTION: Prevent modification of protected users (super admin)
        if user.is_protected:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This user is protected and cannot be modified."
            )
        
        # If demoting from admin, ensure at least one admin remains
        if user.role == UserRole.admin and role_update.role != UserRole.admin:
            # Lock ALL admin rows and count them in application code to prevent race condition
            # This ensures we get an accurate, locked count before committing
            locked_admins = db.query(User).filter(User.role == UserRole.admin).with_for_update().all()
            admin_count = len(locked_admins)
            
            # Recheck after acquiring locks on all admin rows
            if admin_count <= 1:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Cannot demote the last admin. At least one admin must remain."
                )
        
        # Update role
        user.role = role_update.role
        db.commit()
        db.refresh(user)
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user role: {str(e)}"
        )
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        display_name=user.display_name,
        tagline=user.tagline,
        bio=user.bio,
        avatar_url=user.avatar_url,
        role=user.role,
        is_protected=user.is_protected,
        created_at=user.created_at
    )


@router.delete("/users/{user_id}")
def delete_user(
    user_id: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete a user - accessible by admin only"""
    
    # Prevent admin from deleting themselves
    if str(user_id) == str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete yourself."
        )
    
    try:
        # Find user with row-level lock
        user = db.query(User).filter(User.id == user_id).with_for_update().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # PROTECTION: Prevent deletion of protected users (super admin)
        if user.is_protected:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This user is protected and cannot be deleted."
            )
        
        # If deleting an admin, ensure at least one admin remains
        if user.role == UserRole.admin:
            # Lock ALL admin rows and count them
            locked_admins = db.query(User).filter(User.role == UserRole.admin).with_for_update().all()
            admin_count = len(locked_admins)
            
            if admin_count <= 1:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Cannot delete the last admin. At least one admin must remain."
                )
        
        # Delete user (cascades to resources due to relationship configuration)
        db.delete(user)
        db.commit()
        
        return {"success": True, "message": f"User {user.email} deleted successfully"}
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        )
