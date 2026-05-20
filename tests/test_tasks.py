import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from app.core.security import create_access_token
from app.models.task import Task
from app.services.user_service import create_user, get_user_by_email


@pytest.fixture
def auth_headers(client: TestClient, db_session):
    """
    Creates (or reuses) a user and returns JWT auth headers for testing.

    This fixture is idempotent and safe to run multiple times,
    even if the user already exists in the test database.
    """
    email = "taskuser@test.com"
    password = "pass123"

    try:
        user = create_user(db_session, email=email, password=password)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        user = get_user_by_email(db_session, email=email)
        if not user:
            raise RuntimeError(f"Failed to retrieve user {email} after IntegrityError")

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"Authorization": f"Bearer {token}"}


def test_create_task(client, auth_headers):
    """Tests creation of a new task."""
    response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "My task",
            "description": "Test description",
            "is_done": False,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My task"
    assert "id" in data
    assert "owner_id" in data


def test_list_tasks_empty(client, auth_headers):
    """Tests listing tasks when none exist."""
    response = client.get("/tasks", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_with_data(client, auth_headers, db_session):
    """Tests listing tasks when data exists."""
    user = get_user_by_email(db_session, "taskuser@test.com")

    task1 = Task(title="Task 1", owner_id=user.id)
    task2 = Task(title="Task 2", owner_id=user.id, is_done=True)

    db_session.add_all([task1, task2])
    db_session.commit()

    response = client.get("/tasks", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert all(t["owner_id"] == user.id for t in data)


def test_get_task_success(client, auth_headers, db_session):
    """Tests retrieving a task by ID."""
    user = get_user_by_email(db_session, "taskuser@test.com")

    task = Task(title="Specific task", owner_id=user.id)
    db_session.add(task)
    db_session.commit()

    response = client.get(f"/tasks/{task.id}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["title"] == "Specific task"


def test_get_task_not_found(client, auth_headers):
    """Tests retrieving a non-existent task."""
    response = client.get("/tasks/99999", headers=auth_headers)

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_task_other_user(client, auth_headers, db_session):
    """Tests that a user cannot access another user's tasks."""
    from app.services.user_service import create_user as create_svc_user

    other_user = create_svc_user(db_session, email="other@test.com", password="pass123")
    db_session.commit()

    task = Task(title="Secret task", owner_id=other_user.id)
    db_session.add(task)
    db_session.commit()

    response = client.get(f"/tasks/{task.id}", headers=auth_headers)

    assert response.status_code == 404


def test_update_task(client, auth_headers, db_session):
    """Tests updating an existing task."""
    user = get_user_by_email(db_session, "taskuser@test.com")

    task = Task(title="Old", description="Old description", owner_id=user.id)
    db_session.add(task)
    db_session.commit()

    response = client.put(
        f"/tasks/{task.id}",
        headers=auth_headers,
        json={"title": "Updated", "is_done": True},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Updated"
    assert data["is_done"] is True
    assert data["description"] == "Old description"


def test_delete_task(client, auth_headers, db_session):
    """Tests deleting a task."""
    user = get_user_by_email(db_session, "taskuser@test.com")

    task = Task(title="To delete", owner_id=user.id)
    db_session.add(task)
    db_session.commit()

    response = client.delete(f"/tasks/{task.id}", headers=auth_headers)

    assert response.status_code == 204

    response = client.get(f"/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == 404


def test_create_task_without_auth(client):
    """Tests that protected routes reject unauthenticated requests."""
    response = client.post(
        "/tasks",
        json={"title": "No auth"},
    )

    assert response.status_code == 401
