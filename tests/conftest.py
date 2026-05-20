import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db.session import get_db
from app.models import Base

TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/taskmanager_test"

engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"sslmode": "disable"},
    poolclass=StaticPool,
)

SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Cria as tabelas uma vez no início dos testes e remove no final."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def db_session():
    """
    Fixture de sessão com transação + rollback para isolamento total entre testes.
    Cada teste roda em sua própria transação que é revertida ao final.
    """
    connection = engine_test.connect()
    transaction = connection.begin()
    
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    
    try:
        yield session
    finally:
        transaction.rollback()
        session.close()
        connection.close()


@pytest.fixture
def client(db_session: Session):
    """
    TestClient com override do get_db para usar a sessão de teste com rollback.
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