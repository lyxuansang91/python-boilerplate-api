import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine

from app.core.db import get_session
from app.main import app
from app.models import Base

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DB = "stockbot_test"

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL, echo=True)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session():
    """Mở session database test (reset sau mỗi test)."""
    with Session(engine) as session:
        yield session
        session.rollback()


@pytest.fixture(scope="function")
def client(db_session: Session):
    """Client test với database test."""

    def override_get_session():
        return db_session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
