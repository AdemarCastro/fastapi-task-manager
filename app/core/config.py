from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Task Manager"
    APP_ENV: str = "development"
    APP_NAME: str = "TaskManager"
    APP_DEBUG: bool = True
    VERSION: str = "0.1.0"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5433/taskmanager"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
