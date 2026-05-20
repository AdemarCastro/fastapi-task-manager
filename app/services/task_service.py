from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

def get_tasks_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_task_by_id_and_owner(db: Session, task_id: int, owner_id: int) -> Task | None:
    return (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == owner_id)
        .first()
    )

def create_task(db: Session, task_in: TaskCreate, owner_id: int) -> Task:
    task = Task(**task_in.model_dump(), owner_id=owner_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, task: Task, task_in: TaskUpdate) -> Task:
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: Task) -> bool:
    db.delete(task)
    db.commit()
    return True