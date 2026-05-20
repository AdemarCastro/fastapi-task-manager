# FastAPI Task Manager

<div align="center">

[![CI](https://github.com/AdemarCastro/fastapi-task-manager/actions/workflows/ci.yml/badge.svg)](https://github.com/AdemarCastro/fastapi-task-manager/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688)](https://fastapi.tiangolo.com)
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

🔗 **Live Demo — Swagger UI**  
https://fastapi-task-manager-9z7w.onrender.com/docs

> ⚠️ The instance may take a few seconds to wake up (cold start on free tier).

</div>

---

## Features

| Category | Details |
|----------|---------|
| 🔐 **Authentication** | JWT access + refresh tokens, bcrypt password hashing |
| ✅ **Tasks** | Full CRUD with per-user data isolation |
| 🗄️ **Database** | PostgreSQL, SQLAlchemy 2.0 ORM, Alembic migrations |
| 🧪 **Testing** | pytest + httpx, 90%+ coverage |
| 🚀 **DevOps** | Docker, Docker Compose, GitHub Actions CI |
| 📖 **Documentation** | Auto-generated Swagger/OpenAPI |
| 🧹 **Code Quality** | Ruff (lint + format) |

---

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Backend** | FastAPI, Python 3.10, Uvicorn |
| **Database** | PostgreSQL 16, SQLAlchemy 2.0, Alembic |
| **Auth** | python-jose (JWT), bcrypt, passlib |
| **Testing** | pytest, httpx, TestClient |
| **DevOps** | Docker, Docker Compose, GitHub Actions |
| **Quality** | Ruff (lint + format), Pydantic v2 |

---

## Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- Git

### 1 — Clone the repository

```bash
git clone https://github.com/AdemarCastro/fastapi-task-manager.git
cd fastapi-task-manager
```

### 2 — Create virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Start database

```bash
docker compose up -d db

# Wait ~10 seconds for PostgreSQL to be ready
```

### 5 — Run migrations

```bash
alembic upgrade head
```

### 6 — Run application

```bash
uvicorn app.main:app --reload
```

Application will be available at:

```
http://localhost:8000
```

Swagger documentation:

```
http://localhost:8000/docs
```

---

## Environment Variables

Copy `.env.example` to `.env` for local development:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/taskmanager

# Authentication
SECRET_KEY=your-secret-key-min-32-chars-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

> 🔐 **Never commit `.env` to version control.** Use secrets management in production.

---

## Authentication Flow (Swagger UI)

With the updated HTTP Bearer configuration:

### 1. Login
* Open `POST /auth/login`
* Click **Try it out**
* Send JSON:
```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

### 2. Copy token
* Copy only the `access_token` string from response (starts with `eyJ...`)

### 3. Authorize Swagger
* Click 🔒 **Authorize** (top right button)
* Paste the token **(Swagger adds `Bearer ` prefix automatically)**
* Click **Authorize** → **Close**
* 🔐 The lock icon should now show as "authorized"

### 4. Test protected routes
* Now you can access `/tasks` endpoints directly in Swagger UI

### Refresh Token (Optional)
When access token expires (30 min), use `/auth/refresh`:

```bash
curl -X POST https://fastapi-task-manager-9z7w.onrender.com/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "your_refresh_token_here"}'
```

---

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_auth.py -v
```

---

## Project Structure

```
fastapi-task-manager/
├── app/
│   ├── api/              # Route handlers (auth, tasks)
│   ├── core/             # Config, security, auth dependencies
│   ├── db/               # Database connection and session
│   ├── models/           # SQLAlchemy ORM models
│   ├── schemas/          # Pydantic schemas for validation
│   ├── services/         # Business logic layer
│   └── main.py           # Application entry point
├── tests/                # pytest test suite
│   ├── conftest.py       # Test fixtures and configuration
│   ├── test_auth.py      # Authentication tests
│   └── test_tasks.py     # Task CRUD tests
├── alembic/              # Database migrations
│   └── versions/         # Migration files
├── .github/
│   └── workflows/
│       └── ci.yml        # GitHub Actions CI/CD
├── .env.example          # Example environment variables
├── .dockerignore         # Docker ignore rules
├── docker-compose.yml    # Local development setup
├── Dockerfile            # Production Docker image
├── render.yaml           # Render Blueprint configuration
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Tooling config (ruff, pytest)
├── alembic.ini           # Alembic configuration
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

---

## API Documentation

Once running, visit the interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Key Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/health` | Health check | No |
| POST | `/auth/register` | Create new user | No |
| POST | `/auth/login` | Get JWT tokens | No |
| POST | `/auth/refresh` | Refresh access token | No |
| GET | `/tasks` | List user's tasks | Yes |
| POST | `/tasks` | Create new task | Yes |
| GET | `/tasks/{id}` | Get specific task | Yes |
| PUT | `/tasks/{id}` | Update task | Yes |
| DELETE | `/tasks/{id}` | Delete task | Yes |

---

## Deployment

This project is ready to deploy to:

- ✅ **Render** (using `render.yaml` Blueprint)
- ✅ **Railway**
- ✅ **Fly.io**
- ✅ **AWS** (ECS, App Runner)
- ✅ **GCP Cloud Run**

### Required Environment Variables

```env
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
PORT=8000
```

### Deploy to Render (Recommended)

1. Create account at [render.com](https://render.com)
2. Connect your GitHub repository
3. Render will auto-detect `render.yaml`
4. Configure environment variables
5. Deploy!

---

## Development

### Code Quality

```bash
# Lint code
ruff check app/ tests/

# Auto-fix issues
ruff check app/ tests/ --fix

# Format code
ruff format app/ tests/
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View current migration status
alembic current
```

---

## Contributing

### Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `refactor:` code improvements
- `test:` add or update tests
- `ci:` CI/CD changes
- `chore:` tooling/maintenance

### Example

```bash
git commit -m "feat: add refresh token endpoint"
git commit -m "fix: resolve database connection timeout"
git commit -m "docs: update README authentication flow"
```

---

## Testing in Production

After deployment, test your live API:

```bash
# Health check
curl https://your-api.onrender.com/health

# Register user
curl -X POST https://your-api.onrender.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123!"}'

# Login
curl -X POST https://your-api.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123!"}'
```

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- [Render](https://render.com/) - Cloud hosting platform
- [pytest](https://docs.pytest.org/) - Testing framework

---

<div align="center">

**Made by [Ademar Castro](https://github.com/AdemarCastro)**

[🔗 Portfolio](https://ademar-castro.duckdns.org/) · [💼 LinkedIn](https://www.linkedin.com/in/ademar-castro-8bb95b256/)

</div>