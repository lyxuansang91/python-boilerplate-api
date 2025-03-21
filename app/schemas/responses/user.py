from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int | None
    email: str
    is_active: bool | None
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        from_attributes = True
