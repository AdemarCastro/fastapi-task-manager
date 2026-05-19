# FastAPI Task Manager

REST API completa com autenticação JWT, refresh token, CRUD de tarefas e versionamento de banco com Alembic.

## 🚀 Stack
- **Backend:** FastAPI + Python 3.11+
- **Auth:** JWT (python-jose) + bcrypt
- **DB:** PostgreSQL + SQLAlchemy + Alembic
- **Testes:** pytest + httpx
- **Infra:** Docker + Docker Compose

## 📦 Setup
```bash
git clone https://github.com/SEU-USUARIO/P01-fastapi-jwt-pg.git
cd P01-fastapi-jwt-pg
docker compose up -d --build
```

## 📘 Documentação
Acesse o Swagger UI em: http://localhost:8000/docs

## 🧪 Testes
```bash
docker compose exec api pytest
```
