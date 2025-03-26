import pytest
from fastapi.testclient import TestClient
from app.core.config import settings
from sqlmodel import Session, select, delete
from app.models import User


@pytest.mark.parametrize(
    "invalid_email",
    [
        "plainaddress",
        "@missingusername.com",
        "username@.com",
        "username@com",
        "username@domain..com",
    ],
)
def test_register_user_invalid_email(
    db_session: Session, client: TestClient, invalid_email
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={
            "email": invalid_email,
            "password": "password123",
        },
    )
    assert r.status_code == 422
