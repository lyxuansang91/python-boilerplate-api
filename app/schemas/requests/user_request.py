from pydantic import BaseModel, EmailStr
class UpdateUserRequest(BaseModel):
    password: str | None = None