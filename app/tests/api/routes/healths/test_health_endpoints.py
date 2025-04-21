import pytest
from fastapi.testclient import TestClient

from app.core.config import settings


@pytest.mark.parametrize(
    "endpoint, expected_status",
    [
        ("healths/liveness", {"status": "UP"}),
        ("healths/readiness", {"status": "UP"}),
    ],
)
def test_health_endpoints(client: TestClient, endpoint, expected_status) -> None:
    url = f"{settings.API_V1_STR}/{endpoint}"
    r = client.get(url)
    assert r.status_code == 200
    assert r.json() == expected_status
