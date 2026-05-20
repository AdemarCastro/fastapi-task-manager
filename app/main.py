from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="REST API for task management with JWT authentication.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={"persistAuthorization": True},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://fastapi-task-manager-9z7w.onrender.com",
        "https://fastapi-task-manager.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api import auth, tasks
app.include_router(auth.router, tags=["Authentication"])
app.include_router(tasks.router, tags=["Tasks"])

@app.get(
    "/health",
    tags=["System"],
    summary="Health check",
    description="Checks if the API is running and operational.",
)
def health_check():
    """
    Health check endpoint.

    Returns the current status of the API to verify if the service
    is running correctly.
    """
    return {"status": "ok", "message": "API is running"}