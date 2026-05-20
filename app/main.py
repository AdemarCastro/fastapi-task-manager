from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles

from app.api import auth, tasks
from app.core.config import settings

security = HTTPBearer()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="REST API for task management with JWT authentication.",
    docs_url=None,
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://fastapi-task-manager-9z7w.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Authentication"])
app.include_router(tasks.router, tags=["Tasks"])


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{settings.PROJECT_NAME} - Docs",
        swagger_css_url="/static/swagger-dark.css",
        swagger_ui_parameters={
            "displayRequestDuration": True,
            "persistAuthorization": True,
            "defaultModelsExpandDepth": -1,
        },
    )


@app.get("/docs/oauth2-redirect", include_in_schema=False)
def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get(
    "/health",
    tags=["System"],
    summary="Health check",
    description="Checks if the API is running and operational.",
)
def health_check():
    return {
        "status": "ok",
        "message": "API is running",
    }
