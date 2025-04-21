import pytest  # noqa: I001
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.core.config import settings
from app.tests.utils.test_get_users_invalid_auth import check_authentication_errors


@pytest.fixture
def admin_token(client: TestClient):
    return get_token(client, "admin@example.com", "123456")


@pytest.fixture
def valid_user_token(client: TestClient):
    return get_token(client, "user@example.com", "123456")


def get_token(client: TestClient, email: str, password: str) -> str:
    login_url = f"{settings.API_V1_STR}/auth/login"
    response = client.post(login_url, json={"email": email, "password": password})
    assert response.status_code == 200, f"Login failed for {email}"
    return f"Bearer {response.json()['access_token']}"


def test_get_users_invalid_auth(
    client: TestClient, admin_token: str, valid_user_token: str
):
    url = f"{settings.API_V1_STR}/users"
    params = {"page": 1, "limit": 10}

    test_cases = [
        {"headers": None, "expected_status": 401},
        {"headers": "user", "expected_status": 403},
        {"headers": "invalid", "expected_status": 401},
    ]

    for case in test_cases:
        check_authentication_errors(
            client=client,
            method="GET",
            url=url,
            admin_token=admin_token,
            valid_user_token=valid_user_token,
            params=params,
            **case,
        )


@pytest.mark.parametrize(
    "page, limit, headers, expected_status, expected_keys",
    [
        (1, 10, "admin", 200, ["items", "total", "page", "size", "pages"]),
        (1, 0, "admin", 422, None),  # limit không hợp lệ
        (-1, 10, "admin", 422, None),  # page không hợp lệ
    ],
)
def test_get_users(
    client: TestClient,
    db_session: Session,
    admin_token: str,
    valid_user_token: str,
    page: int,
    limit: int,
    headers: str | None,
    expected_status: int,
    expected_keys: list[str] | None,
):
    url = f"{settings.API_V1_STR}/users?page={page}&limit={limit}"

    headers_map = {
        "admin": {"Authorization": admin_token},
        "user": {"Authorization": valid_user_token},
        "invalid": {"Authorization": "invalid_token"},
        None: {},  # Không có token
    }
    response = client.get(url, headers=headers_map[headers])

    assert response.status_code == expected_status

    if expected_status == 200:
        json_response = response.json()
        assert all(key in json_response for key in expected_keys)
        assert isinstance(json_response["items"], list)
        assert isinstance(json_response["total"], int)
        assert isinstance(json_response["page"], int)
        assert isinstance(json_response["size"], int)
        assert isinstance(json_response["pages"], int)

        for user in json_response["items"]:
            assert "id" in user
            assert "email" in user
            assert "is_active" in user
            assert "created_at" in user
            assert "updated_at" in user
