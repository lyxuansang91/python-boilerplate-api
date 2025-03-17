from pydantic import BaseModel, Field

# from sqlmodel import SQLModel


class CurrentUser(BaseModel):
    id: int = Field(None, description="User ID")

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
