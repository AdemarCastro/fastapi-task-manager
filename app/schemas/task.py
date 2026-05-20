from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str = Field(..., example="Estudar FastAPI", description="Título da tarefa")
    description: str | None = Field(
        None, example="Completar o projeto P01", description="Detalhes opcionais"
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
    id: int = Field(..., example=1)
    owner_id: int = Field(..., example=10)
    created_at: datetime
    updated_at: datetime
