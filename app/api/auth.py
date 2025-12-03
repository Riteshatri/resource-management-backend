from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token, RegisterResponse, LoginRequest
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from app.db.seed import seed_default_resources

router = APIRouter()


@router.post("/signup", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        display_name=user_data.display_name,
        bio=user_data.bio,
        avatar_url=user_data.avatar_url
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Seed default resources for new user
    seed_default_resources(db, str(new_user.id))
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )
    
    # Convert UUID to string for response
    user_response = UserResponse(
        id=str(new_user.id),
        email=new_user.email,
        display_name=new_user.display_name,
        bio=new_user.bio,
        avatar_url=new_user.avatar_url,
        role=new_user.role,
        created_at=new_user.created_at
    )
    
    return RegisterResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )


@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout():
    # Token invalidation would be handled client-side by removing the token
    # For stateless JWT, we just return success
    return {"message": "Logged out successfully"}
