from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.database import Base


class ResourceIcon(str, enum.Enum):
    SERVER = "server"
    GLOBE = "globe"
    LINK = "link"
    DATABASE = "database"
    HARD_DRIVE = "hard_drive"
    NETWORK = "network"
    KEY = "key"
    BOX = "box"
    FOLDER_OPEN = "folder_open"


class ResourceStatus(str, enum.Enum):
    RUNNING = "Running"
    STOPPED = "Stopped"
    PENDING = "Pending"


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    icon = Column(String(20), nullable=False)
    title = Column(String(100), nullable=False)
    resource_name = Column(String(200), nullable=False)
    description = Column(String(500))
    status = Column(String(20), default=ResourceStatus.RUNNING.value)
    region = Column(String(50), default="East US")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="resources")
