import pytest  # noqa: I001
from fastapi.testclient import TestClient
from app.core.config import settings


@pytest.fixture
def user_token(client: TestClient):
    return get_token(client, "user@example.com", "123456")


def get_token(client: TestClient, email: str, password: str) -> str:
    login_url = f"{settings.API_V1_STR}/auth/login"
    response = client.post(login_url, json={"email": email, "password": password})
    assert response.status_code == 200, f"Login failed for {email}"
    return f"Bearer {response.json()['access_token']}"


def test_get_me(client: TestClient, user_token: str):
    url = f"{settings.API_V1_STR}/auth/me"

    response = client.get(url, headers={"Authorization": user_token})

    assert response.status_code == 200
    json_response = response.json()

    assert isinstance(json_response, dict)
    assert "id" in json_response
    assert json_response["email"] == "user@example.com"
    assert isinstance(json_response["is_active"], bool)
    assert "created_at" in json_response
    assert "updated_at" in json_response
