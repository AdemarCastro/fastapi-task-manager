from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.auth_deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import (
    create_task,
    delete_task,
    get_task_by_id_and_owner,
    get_tasks_by_user,
    update_task,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lista todas as tarefas do usuário autenticado (com paginação)."""
    return get_tasks_by_user(db, user_id=current_user.id, skip=skip, limit=limit)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cria uma nova tarefa para o usuário autenticado."""
    return create_task(db, task_in=task_in, owner_id=current_user.id)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtém uma tarefa específica do usuário autenticado."""
    task = get_task_by_id_and_owner(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_existing_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Atualiza uma tarefa específica do usuário autenticado."""
    task = get_task_by_id_and_owner(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return update_task(db, task=task, task_in=task_in)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Exclui uma tarefa específica do usuário autenticado."""
    task = get_task_by_id_and_owner(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    delete_task(db, task=task)
    return None
