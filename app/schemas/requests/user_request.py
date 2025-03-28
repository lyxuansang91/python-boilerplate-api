from typing import Literal

from pydantic import BaseModel, EmailStr


class UpdateUserRequest(BaseModel):
    password: str | None = None

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    role: Literal["admin", "user"] = "user"
