from pydantic import Field, SQLModel


class CurrentUser(SQLModel):
    id: int = Field(None, description="User ID")

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
