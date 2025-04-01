from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    id: int | None
    email: EmailStr
    is_active: bool | None
    created_at: datetime | None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class UserResponseWithRole(UserResponse):
    role: str | None
