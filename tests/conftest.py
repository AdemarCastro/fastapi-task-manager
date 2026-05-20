import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import get_db
from app.main import app
from app.models import Base

# -------------------------------------------------------------------
# DATABASE CONFIG (ENV-FIRST + FALLBACK)
# -------------------------------------------------------------------
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5433/taskmanager_test",
)

ADMIN_DATABASE_URL = os.getenv(
    "ADMIN_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5433/postgres",
)


# -------------------------------------------------------------------
# ADMIN ENGINE (used to create test DB if needed)
# -------------------------------------------------------------------
admin_engine = create_engine(
    ADMIN_DATABASE_URL,
    connect_args={"sslmode": "disable"},
)


def create_test_database_if_not_exists():
    """Creates the test database if it does not already exist."""
    try:
        if os.getenv("GITHUB_ACTIONS") == "true":
            return

        with admin_engine.connect() as conn:
            conn = conn.execution_options(isolation_level="AUTOCOMMIT")

            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = 'taskmanager_test'")
            ).scalar()

            if not result:
                conn.execute(text("CREATE DATABASE taskmanager_test"))

    except Exception:
        # Ignore failures (CI environments, limited permissions, etc.)
        pass


@pytest.fixture(scope="session", autouse=True)
def ensure_test_db_exists():
    """Ensures the test database exists before running the test suite."""
    create_test_database_if_not_exists()
    yield


# -------------------------------------------------------------------
# TEST ENGINE
# -------------------------------------------------------------------
engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"sslmode": "disable"},
    poolclass=StaticPool,
)

SessionTest = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test,
)


# -------------------------------------------------------------------
# DB LIFECYCLE
# -------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Creates all tables before tests and drops them after."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def db_session():
    """
    Provides a transactional database session with full rollback isolation.
    Ensures complete test independence.
    """
    connection = engine_test.connect()
    transaction = connection.begin()

    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    try:
        yield session
    finally:
        transaction.rollback()
        session.close()
        connection.close()


# -------------------------------------------------------------------
# FASTAPI CLIENT
# -------------------------------------------------------------------
@pytest.fixture
def client(db_session: Session):
    """
    FastAPI TestClient with dependency override for get_db,
    using a transactional test database session.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


# -------------------------------------------------------------------
# PYTEST CONFIG
# -------------------------------------------------------------------
def pytest_configure(config):
    """
    Global pytest configuration hook.
    Suppresses known deprecation warnings (e.g., pydantic).
    """
    import warnings

    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        module="pydantic",
    )
