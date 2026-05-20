import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from app.core.security import get_password_hash, create_access_token
from app.models.user import User
from app.models.task import Task
from app.services.user_service import get_user_by_email, create_user

@pytest.fixture
def auth_headers(client: TestClient, db_session):
    """
    Cria (ou reutiliza) um usuário e retorna headers com token JWT para testes.
    Idempotente: funciona mesmo se o usuário já existir no banco de teste.
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
    response = client.post(
        "/tasks",
        headers=auth_headers,
        json={"title": "Minha tarefa", "description": "Descrição teste", "is_done": False}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Minha tarefa"
    assert "id" in data
    assert "owner_id" in data


def test_list_tasks_empty(client, auth_headers):
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_with_data(client, auth_headers, db_session):
    user = get_user_by_email(db_session, "taskuser@test.com")
    
    task1 = Task(title="Tarefa 1", owner_id=user.id)
    task2 = Task(title="Tarefa 2", owner_id=user.id, is_done=True)
    db_session.add_all([task1, task2])
    db_session.commit()
    
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(t["owner_id"] == user.id for t in data)


def test_get_task_success(client, auth_headers, db_session):
    user = get_user_by_email(db_session, "taskuser@test.com")
    task = Task(title="Tarefa específica", owner_id=user.id)
    db_session.add(task)
    db_session.commit()
    
    response = client.get(f"/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Tarefa específica"


def test_get_task_not_found(client, auth_headers):
    response = client.get("/tasks/99999", headers=auth_headers)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_task_other_user(client, auth_headers, db_session):
    from app.services.user_service import create_user as create_svc_user
    other_user = create_svc_user(db_session, email="other@test.com", password="pass123")
    db_session.commit()
    
    task = Task(title="Tarefa secreta", owner_id=other_user.id)
    db_session.add(task)
    db_session.commit()
    
    response = client.get(f"/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == 404


def test_update_task(client, auth_headers, db_session):
    user = get_user_by_email(db_session, "taskuser@test.com")
    task = Task(title="Antigo", description="Velha", owner_id=user.id)
    db_session.add(task)
    db_session.commit()
    
    response = client.put(
        f"/tasks/{task.id}",
        headers=auth_headers,
        json={"title": "Atualizado", "is_done": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Atualizado"
    assert data["is_done"] is True
    assert data["description"] == "Velha"


def test_delete_task(client, auth_headers, db_session):
    user = get_user_by_email(db_session, "taskuser@test.com")
    task = Task(title="Para deletar", owner_id=user.id)
    db_session.add(task)
    db_session.commit()
    
    response = client.delete(f"/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == 204
    
    response = client.get(f"/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == 404


def test_create_task_without_auth(client):
    """Testa que rota protegida rejeita requisição sem token."""
    response = client.post("/tasks", json={"title": "Sem auth"})
    assert response.status_code == 401