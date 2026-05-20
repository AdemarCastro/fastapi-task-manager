from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    Provides a SQLAlchemy database session.

    This function is used as a FastAPI dependency and ensures that:
    - A new database session is created per request
    - The session is properly closed after the request lifecycle

    Yields:
        Session: SQLAlchemy database session instance
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
