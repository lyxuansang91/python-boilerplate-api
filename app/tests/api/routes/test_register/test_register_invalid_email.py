import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings


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
    _: Session, client: TestClient, invalid_email
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={
            "email": invalid_email,
            "password": "password123",
        },
    )
    assert r.status_code == 422
