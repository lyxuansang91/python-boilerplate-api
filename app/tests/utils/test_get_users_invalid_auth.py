import pytest  # noqa: I001
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "auth_params",
    [
        {"headers": None, "expected_status": 401},  # Không có Token
        {"headers": "user", "expected_status": 403},  # User thường không có quyền
        {"headers": "invalid", "expected_status": 401},  # Token không hợp lệ
    ],
)
def check_authentication_errors(**kwargs):
    client = kwargs.get("client")
    method = kwargs.get("method")
    url = kwargs.get("url")
    headers_key = kwargs.get("headers")
    expected_status = kwargs.get("expected_status")
    admin_token = kwargs.get("admin_token")
    valid_user_token = kwargs.get("valid_user_token")
    params = kwargs.get("params")
    json = kwargs.get("json")

    headers_map = {
        None: {},
        "invalid": {"Authorization": "invalid_token"},
        "user": {"Authorization": valid_user_token} if valid_user_token else {},
        "admin": {"Authorization": admin_token} if admin_token else {},
    }

    request_headers = headers_map.get(headers_key, {})
    request_func = getattr(client, method.lower(), None)
    if request_func is None:
        raise ValueError(f"Method '{method}' is not supported")

    if method.upper() == "GET":
        response = request_func(url, headers=request_headers, params=params)
    else:
        response = request_func(url, headers=request_headers, params=params, json=json)

    assert response.status_code == expected_status
