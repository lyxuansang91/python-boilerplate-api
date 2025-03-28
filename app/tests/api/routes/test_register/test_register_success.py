from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.config import settings
from app.models import User


def test_register_success(db_session: Session, client: TestClient) -> None:
    user_data = {
        "email": "pollo@gmail.com",
        "password": "password123",
    }

    url = f"{settings.API_V1_STR}/auth/register"

    # Delete the user if it already exists to avoid duplicate email errors
    existing_user = db_session.exec(
        select(User).where(User.email == user_data["email"])
    ).first()
    if existing_user:
        db_session.delete(existing_user)
        db_session.commit()

    response = client.post(url, json=user_data)
    assert response.status_code == 201

    data = response.json()

    # Validate response fields
    assert "id" in data and isinstance(
        data["id"], int
    ), "Response JSON does not contain a valid 'id'"
    assert data["email"] == user_data["email"], "Email mismatch"
    assert data["is_active"] is True, "User should be active by default"
    assert "created_at" in data and isinstance(
        data["created_at"], str
    ), "Missing or invalid 'created_at'"
    assert "updated_at" in data and isinstance(
        data["updated_at"], str
    ), "Missing or invalid 'updated_at'"

    # Verify the user exists in the database
    user = db_session.exec(select(User).where(User.id == data["id"])).first()
    assert user is not None, "User was not created in the database"
    assert user.email == user_data["email"]
    assert user.is_active is True
