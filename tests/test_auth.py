import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import engine, SessionLocal, Base
from app.core.security import get_password_hash
from app.models.user import User

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_register_user(client):
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "strongpass123"
    })
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"

def test_register_duplicate_email(client):
    client.post("/auth/register", json={"email": "dup@example.com", "password": "pass123"})
    response = client.post("/auth/register", json={"email": "dup@example.com", "password": "pass456"})
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_login_success(client, db):
    user = User(email="login@test.com", hashed_password=get_password_hash("pass123"))
    db.add(user)
    db.commit()
    
    response = client.post("/auth/login", json={"email": "login@test.com", "password": "pass123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"