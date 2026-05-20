from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    """
    Base schema for task data.

    Contains shared fields used across create, update, and response schemas.
    """

    title: str = Field(
        ...,
        description="Task title",
        json_schema_extra={"example": "Study FastAPI"},
    )
    description: str | None = Field(
        None,
        description="Optional task details",
        json_schema_extra={"example": "Complete P01 project"},
    )
    is_done: bool = Field(
        False,
        description="Completion status",
    )


class TaskCreate(TaskBase):
    """
    Schema used for creating a new task.
    """

    pass


class TaskUpdate(BaseModel):
    """
    Schema used for updating an existing task.

    All fields are optional to allow partial updates.
    """

    title: str | None = Field(
        None,
        description="Updated task title",
    )
    description: str | None = Field(
        None,
        description="Updated task description",
    )
    is_done: bool | None = Field(
        None,
        description="Updated completion status",
    )


class TaskResponse(TaskBase):
    """
    Schema returned by the API when retrieving tasks.

    Includes database-generated fields such as id and timestamps.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        json_schema_extra={"example": 1},
    )
    owner_id: int = Field(
        ...,
        json_schema_extra={"example": 10},
    )
    created_at: datetime
    updated_at: datetime
