from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    id: int | None
    email: EmailStr
    is_active: bool | None
    created_at: datetime | None
    updated_at: datetime | None
    first_name: str | None
    last_name: str | None
    address: str | None

    model_config = ConfigDict(from_attributes=True)


class UserResponseWithRole(UserResponse):
    role: str | None
