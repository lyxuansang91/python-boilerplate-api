import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, select

from app.core import security
from app.deps import get_db
from app.main import app
from app.models import Base, User, UserRole

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DB_TEST = os.getenv("POSTGRES_DB_TEST", "stockbot_test")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB_TEST}"

engine = create_engine(DATABASE_URL, echo=True)


@pytest.fixture(scope="function")
def db_session():
    """Mở session database test (reset sau mỗi test)."""
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
        session.rollback()
    Base.metadata.drop_all(engine)


@pytest.fixture
def sample_users(db_session: Session) -> None:
    """Thêm user mặc định vào database test."""

    default_users_data = [
        {
            "email": "admin@example.com",
            "hash_password": security.get_password_hash("123456"),  # Hash password
            "role": UserRole.ADMIN.value,
            "is_active": True,
        },
        {
            "email": "user@example.com",
            "hash_password": security.get_password_hash("123456"),  # Hash password
            "role": UserRole.USER.value,
            "is_active": True,
        },
    ]

    for user_data in default_users_data:
        existing_user = db_session.exec(
            select(User).where(User.email == user_data["email"])
        ).first()

        if not existing_user:
            db_session.add(User(**user_data))
    db_session.commit()


@pytest.fixture(scope="function")
def client(db_session: Session):
    """Client test với database test."""

    def override_get_session():
        return db_session

    app.dependency_overrides[get_db] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
