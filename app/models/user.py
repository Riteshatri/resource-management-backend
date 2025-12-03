from sqlalchemy import Column, String, DateTime, Boolean, Enum as SQLEnum, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    display_name = Column(String(100), nullable=True)
    tagline = Column(String(200), nullable=True)
    bio = Column(String(500), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.user, nullable=False)
    is_protected = Column(Boolean, default=False, nullable=False)  # Super admin protection flag
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    resources = relationship("Resource", back_populates="user", cascade="all, delete-orphan")


class ThemeConfig(Base):
    __tablename__ = "theme_config"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    config_key = Column(String(100), unique=True, nullable=False)
    config_value = Column(String(2000), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
