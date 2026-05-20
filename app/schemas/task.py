from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str = Field(
        ..., description="Título da tarefa", json_schema_extra={"example": "Estudar FastAPI"}
    )
    description: str | None = Field(
        None,
        description="Detalhes opcionais",
        json_schema_extra={"example": "Completar o projeto P01"},
    )
    is_done: bool = Field(False, description="Status de conclusão")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(None, description="Novo título")
    description: str | None = Field(None, description="Nova descrição")
    is_done: bool | None = Field(None, description="Atualizar status")


class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., json_schema_extra={"example": 1})
    owner_id: int = Field(..., json_schema_extra={"example": 10})
    created_at: datetime
    updated_at: datetime
