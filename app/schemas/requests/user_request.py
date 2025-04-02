from typing import Literal

from pydantic import BaseModel, EmailStr


class UpdateUserRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    role: Literal["admin", "user"] = "user"
