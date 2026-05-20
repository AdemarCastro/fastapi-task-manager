import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import get_db
from app.main import app
from app.models import Base

TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/taskmanager_test"
ADMIN_DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/postgres"

admin_engine = create_engine(
    ADMIN_DATABASE_URL,
    connect_args={"sslmode": "disable"},
)


def create_test_database_if_not_exists():
    """Creates the test database if it does not already exist."""
    with admin_engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")

        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = 'taskmanager_test'")
        ).scalar()

        if not result:
            conn.execute(text("CREATE DATABASE taskmanager_test"))


@pytest.fixture(scope="session", autouse=True)
def ensure_test_db_exists():
    """Ensures the test database exists before running the test suite."""
    create_test_database_if_not_exists()
    yield


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


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Creates all database tables at test startup and drops them at the end."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def db_session():
    """
    Provides a database session with transaction rollback isolation
    to ensure full test independence.
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


def pytest_configure(config):
    """
    Pytest hook for global test configuration.
    Suppresses known deprecation warnings during test execution.
    """
    import warnings

    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        module="pydantic",
    )
