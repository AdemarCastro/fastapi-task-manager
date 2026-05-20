from app.core.security import get_password_hash
from app.models.user import User


def test_register_user(client):
    """Tests user registration endpoint."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "strongpass123",
        },
    )

    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"


def test_register_duplicate_email(client):
    """Tests that registering with an existing email returns an error."""
    client.post(
        "/auth/register",
        json={
            "email": "dup@example.com",
            "password": "pass123",
        },
    )

    response = client.post(
        "/auth/register",
        json={
            "email": "dup@example.com",
            "password": "pass456",
        },
    )

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_success(client, db_session):
    """Tests successful login and token generation."""
    user = User(
        email="login@test.com",
        hashed_password=get_password_hash("pass123"),
    )

    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        json={
            "email": "login@test.com",
            "password": "pass123",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Tests login with invalid credentials."""
    response = client.post(
        "/auth/login",
        json={
            "email": "wrong@test.com",
            "password": "wrongpass",
        },
    )

    assert response.status_code == 401
    assert "invalid credentials" in response.json()["detail"].lower()
