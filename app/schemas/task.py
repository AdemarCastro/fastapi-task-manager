from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    is_done: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_done: bool | None = None

class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime