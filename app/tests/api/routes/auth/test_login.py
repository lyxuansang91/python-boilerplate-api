import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.core.config import settings
from app.models import User
from app.core import security
from sqlmodel import select


@pytest.mark.parametrize(
    "email, password, expected_status, expected_keys",
    [
        (
            "user@example.com",
            "123456",
            200,
            ["access_token", "refresh_token", "token_type"],
        ),
        ("user@example.com", "654321", 400, None),
        ("user@example.com", "some_password", 400, None),
    ],
)
def test_login(client: TestClient, email, password, expected_status, expected_keys):
    url = f"{settings.API_V1_STR}/auth/login"
    response = client.post(url, json={"email": email, "password": password})
    assert response.status_code == expected_status

    if expected_status == 200:
        json_response = response.json()
        for key in expected_keys:
            assert key in json_response


@pytest.fixture
def create_test_user(db_session: Session):
    email = "user@example.com"
    user = db_session.exec(User).where(User.email == email).first()
    if not user:
        user = User(
            email=email,
            hash_password=security.get_password_hash("123456"),
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
    return user
