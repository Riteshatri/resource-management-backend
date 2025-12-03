from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ResourceBase(BaseModel):
    icon: str = Field(..., max_length=50)
    title: str = Field(..., min_length=1, max_length=100)
    resource_name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    status: str = Field(default="Running", max_length=50)
    region: str = Field(default="East US", max_length=50)


class ResourceCreate(ResourceBase):
    created_at: Optional[datetime] = None


class ResourceUpdate(ResourceBase):
    created_at: Optional[datetime] = None


class ResourceResponse(ResourceBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
