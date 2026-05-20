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

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    responses={
        401: {"description": "Não autenticado"},
        403: {"description": "Acesso negado"},
        404: {"description": "Recurso não encontrado"},
    },
)

# ------------------------------------------------------------
# LIST TASKS
# ------------------------------------------------------------
@router.get(
    "",
    response_model=list[TaskResponse],
    summary="Listar tarefas do usuário",
    description=(
        "Retorna todas as tarefas pertencentes ao usuário autenticado.\n\n"
        "Suporta paginação via `skip` e `limit`."
    ),
)
def list_tasks(
    skip: int = Query(0, ge=0, description="Número de registros para pular (paginação)"),
    limit: int = Query(100, ge=1, le=100, description="Quantidade máxima de tarefas retornadas"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_tasks_by_user(db, user_id=current_user.id, skip=skip, limit=limit)


# ------------------------------------------------------------
# CREATE TASK
# ------------------------------------------------------------
@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova tarefa",
    description=(
        "Cria uma nova tarefa associada ao usuário autenticado.\n\n"
        "A tarefa será automaticamente vinculada ao `owner_id` do usuário atual."
    ),
)
def create_new_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_task(db, task_in=task_in, owner_id=current_user.id)


# ------------------------------------------------------------
# GET TASK BY ID
# ------------------------------------------------------------
@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Obter tarefa por ID",
    description="Retorna uma tarefa específica pertencente ao usuário autenticado.",
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id_and_owner(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task não encontrada ou não pertence ao usuário",
        )
    return task


# ------------------------------------------------------------
# UPDATE TASK
# ------------------------------------------------------------
@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Atualizar tarefa",
    description=(
        "Atualiza os dados de uma tarefa existente.\n\n"
        "Somente tarefas do usuário autenticado podem ser modificadas."
    ),
)
def update_existing_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id_and_owner(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task não encontrada")
    return update_task(db, task=task, task_in=task_in)


# ------------------------------------------------------------
# DELETE TASK
# ------------------------------------------------------------
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir tarefa",
    description="Remove permanentemente uma tarefa do usuário autenticado.",
)
def delete_existing_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id_and_owner(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task não encontrada")
    delete_task(db, task=task)
    return None