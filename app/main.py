from fastapi import FastAPI
from fastapi.security import HTTPBearer

from app.api import auth, tasks
from app.core.config import settings

security = HTTPBearer()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API REST para gerenciamento de tarefas com autenticação JWT.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(auth.router, tags=["Authentication"])
app.include_router(tasks.router, tags=["Tasks"])


@app.get("/health", tags=["System"])
def health_check():
    """Verifica se a API está operacional."""
    return {"status": "ok", "message": "API is running"}
