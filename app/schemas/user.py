from pydantic import BaseModel, EmailStr, Field, field_serializer
from typing import Optional, Any
from datetime import datetime
from uuid import UUID
from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    display_name: Optional[str] = None
    tagline: Optional[str] = Field(None, max_length=200)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    tagline: Optional[str] = Field(None, max_length=200)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None


class PasswordResetRequest(BaseModel):
    new_password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    id: str
    role: UserRole
    is_protected: bool = False
    created_at: datetime
    
    @field_serializer('id')
    def serialize_id(self, value: Any) -> str:
        if isinstance(value, UUID):
            return str(value)
        return value
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class RegisterResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    email: Optional[str] = None


class ThemeConfigResponse(BaseModel):
    id: str
    config_key: str
    config_value: str
    created_at: datetime
    updated_at: datetime
    
    @field_serializer('id')
    def serialize_id(self, value: Any) -> str:
        if isinstance(value, UUID):
            return str(value)
        return value
    
    class Config:
        from_attributes = True


class ThemeConfigUpdate(BaseModel):
    config_value: str
