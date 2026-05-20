# FastAPI Task Manager

<div align="center">

[![CI](https://github.com/AdemarCastro/fastapi-task-manager/actions/workflows/ci.yml/badge.svg)](https://github.com/AdemarCastro/fastapi-task-manager/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136.1-009688)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.49-d71f00)](https://www.sqlalchemy.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192)](https://www.postgresql.org)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.13.4-e92063)](https://docs.pydantic.dev)
[![Pytest](https://img.shields.io/badge/Pytest-9.0.3-0a9edc)](https://docs.pytest.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ed)](https://www.docker.com)
[![Ruff](https://img.shields.io/badge/Linter-Ruff-2a2a2a)](https://docs.astral.sh/ruff/)
[![Coverage](https://img.shields.io/badge/Coverage-90%25%2B-brightgreen)](https://pytest-cov.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<br/>

**A production-ready REST API for task management**  
built with FastAPI · PostgreSQL · JWT · Docker

<br/>

🔗 **[Live Demo — Swagger UI](https://task-manager-api.onrender.com/docs)**

> ⚠️ The instance may take a few seconds to wake up (cold start on free tier).

</div>

---

## Features

| Category | Details |
|---|---|
| 🔐 **Authentication** | JWT access + refresh tokens, bcrypt password hashing |
| ✅ **Tasks** | Full CRUD with per-user data isolation |
| 🗄️ **Database** | PostgreSQL, SQLAlchemy 2.0 ORM, Alembic migrations |
| 🧪 **Testing** | pytest + httpx, 90%+ coverage |
| 🚀 **DevOps** | Docker, Docker Compose, GitHub Actions CI |
| 📖 **Documentation** | Auto-generated Swagger/OpenAPI |
| 🧹 **Code Quality** | Ruff (lint + format) |

---

## Tech Stack

```
Backend       FastAPI · Python 3.10 · Uvicorn
Database      PostgreSQL 16 · SQLAlchemy 2.0 · Alembic
Auth          python-jose (JWT) · bcrypt
Testing       pytest · httpx
DevOps        Docker · GitHub Actions
Lint          Ruff
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose

### 1 — Clone the repository

```bash
git clone https://github.com/AdemarCastro/fastapi-task-manager.git
cd fastapi-task-manager
```

### 2 — Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Start the database

```bash
docker compose up -d db
```

### 5 — Apply migrations

```bash
alembic upgrade head
```

### 6 — Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs at `http://localhost:8000/docs`.

---

## Authentication Flow

The API uses a standard JWT access + refresh token scheme.

**Register a new account**
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Login and retrieve tokens**
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Authenticate requests**
```http
GET /tasks
Authorization: Bearer <access_token>
```

---

## Running Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## Project Structure

```
fastapi-task-manager/
│
├── app/
│   ├── api/            # Route handlers
│   ├── core/           # Settings, security, dependencies
│   ├── db/             # Database session and engine
│   ├── models/         # SQLAlchemy ORM models
│   ├── schemas/        # Pydantic request/response schemas
│   ├── services/       # Business logic layer
│   └── main.py         # Application entry point
│
├── tests/              # pytest test suite
├── alembic/            # Database migration scripts
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── pyproject.toml      # Ruff configuration
```

---

## Deployment

The API is container-ready and can be deployed to any major cloud platform.

**Compatible platforms:** Render · Railway · Fly.io · AWS ECS · GCP Cloud Run

**Required environment variables:**

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `SECRET_KEY` | Secret key for JWT signing | `openssl rand -hex 32` |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL | `30` |

---

## Contributing

Contributions are welcome! Please follow the conventional commit format:

| Prefix | Purpose |
|---|---|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation update |
| `refactor:` | Code improvement without behaviour change |
| `test:` | Adding or updating tests |
| `chore:` | Tooling, config, or dependency changes |

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

<div align="center">

Made with ♥ by **[Ademar Castro](https://github.com/AdemarCastro)**

</div>
