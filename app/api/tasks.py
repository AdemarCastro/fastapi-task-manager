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
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"},
    },
)


# ------------------------------------------------------------
# LIST TASKS
# ------------------------------------------------------------
@router.get(
    "",
    response_model=list[TaskResponse],
    summary="List user tasks",
    description=(
        "Returns all tasks belonging to the authenticated user.\n\n"
        "Supports pagination using `skip` and `limit`."
    ),
)
def list_tasks(
    skip: int = Query(
        0,
        ge=0,
        description="Number of records to skip (pagination offset)",
    ),
    limit: int = Query(
        100,
        ge=1,
        le=100,
        description="Maximum number of tasks to return",
    ),
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
    summary="Create a new task",
    description=(
        "Creates a new task associated with the authenticated user.\n\n"
        "The task is automatically linked to the current user's `owner_id`."
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
    summary="Get task by ID",
    description="Returns a specific task belonging to the authenticated user.",
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id_and_owner(
        db,
        task_id=task_id,
        owner_id=current_user.id,
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found or does not belong to the user",
        )

    return task


# ------------------------------------------------------------
# UPDATE TASK
# ------------------------------------------------------------
@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description=(
        "Updates an existing task.\n\nOnly tasks owned by the authenticated user can be modified."
    ),
)
def update_existing_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id_and_owner(
        db,
        task_id=task_id,
        owner_id=current_user.id,
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return update_task(db, task=task, task_in=task_in)


# ------------------------------------------------------------
# DELETE TASK
# ------------------------------------------------------------
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Permanently deletes a task belonging to the authenticated user.",
)
def delete_existing_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id_and_owner(
        db,
        task_id=task_id,
        owner_id=current_user.id,
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    delete_task(db, task=task)
    return None
