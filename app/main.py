from fastapi import FastAPI

from app.api import auth, tasks
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, version=settings.VERSION, docs_url="/docs", redoc_url="/redoc"
)

app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}
