from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks_by_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[Task]:
    """
    Retrieves a paginated list of tasks for a specific user.

    Args:
        db (Session): Database session.
        user_id (int): ID of the task owner.
        skip (int): Number of records to skip (pagination offset).
        limit (int): Maximum number of records to return.

    Returns:
        list[Task]: List of tasks belonging to the user.
    """
    return db.query(Task).filter(Task.owner_id == user_id).offset(skip).limit(limit).all()


def get_task_by_id_and_owner(
    db: Session,
    task_id: int,
    owner_id: int,
) -> Task | None:
    """
    Retrieves a task by ID ensuring it belongs to the specified owner.

    Args:
        db (Session): Database session.
        task_id (int): Task identifier.
        owner_id (int): User ID of the owner.

    Returns:
        Task | None: Task if found and owned by the user, otherwise None.
    """
    return db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()


def create_task(
    db: Session,
    task_in: TaskCreate,
    owner_id: int,
) -> Task:
    """
    Creates a new task for a specific user.

    Args:
        db (Session): Database session.
        task_in (TaskCreate): Task creation payload.
        owner_id (int): ID of the user who owns the task.

    Returns:
        Task: The created task instance.
    """
    task = Task(**task_in.model_dump(), owner_id=owner_id)

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def update_task(
    db: Session,
    task: Task,
    task_in: TaskUpdate,
) -> Task:
    """
    Updates an existing task with provided fields.

    Only fields explicitly set in the request will be updated.

    Args:
        db (Session): Database session.
        task (Task): Existing task instance.
        task_in (TaskUpdate): Data to update.

    Returns:
        Task: Updated task instance.
    """
    update_data = task_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task: Task) -> bool:
    """
    Deletes a task from the database.

    Args:
        db (Session): Database session.
        task (Task): Task instance to delete.

    Returns:
        bool: True if deletion was successful.
    """
    db.delete(task)
    db.commit()
    return True
