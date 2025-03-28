import pytest
from fastapi.testclient import TestClient

from app.core.config import settings


@pytest.mark.parametrize(
    "field, payload",
    [
        ("email", {"password": "password123"}),  # Thiếu email
        ("password", {"email": "test@example.com"}),  # Thiếu password
        ("email", {"email": None, "password": "password123"}),  # Email null
        ("password", {"email": "test@example.com", "password": None}),  # Password null
    ],
)
def test_register_user_missing_fields(
    client: TestClient, _: str, payload: dict[str, str]
):
    r = client.post(f"{settings.API_V1_STR}/auth/register", json=payload)

    assert r.status_code == 422
    data = r.json()
    assert "detail" in data
