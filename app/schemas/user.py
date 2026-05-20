from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
    created_at: datetime
