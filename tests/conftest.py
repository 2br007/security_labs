import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.core.security import create_access_token
from app.db.models import Base, User
from app.db.session import get_db
from app.main import app

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@test_db:5432/security_lab_test",
)

engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)

TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """
    True transactional isolation per test (SAFE for FastAPI).
    """

    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    # SAVEPOINT for nested rollback safety
    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(sess, trans):
        nonlocal nested
        if trans.nested and not trans._parent.nested:
            nested = connection.begin_nested()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def create_user(db_session):
    def _create(username: str) -> User:
        user = User(username=username, email=f"{username}@test.com")
        db_session.add(user)
        db_session.flush()  # no commit needed
        db_session.refresh(user)
        return user

    return _create


@pytest.fixture
def auth_token():
    def _create(user_id: int):
        return create_access_token({"sub": str(user_id)})

    return _create


@pytest.fixture
def auth_headers(auth_token):
    def _headers(user_id: int):
        token = auth_token(user_id)
        return {"Authorization": f"Bearer {token}"}

    return _headers


@pytest.fixture
def mock_httpx():
    with patch("app.api.vulnerable.ssrf.httpx.AsyncClient") as mock:
        instance = mock.return_value.__aenter__.return_value
        yield instance
