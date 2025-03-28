from pydantic import BaseModel, ConfigDict, Field

# from sqlmodel import SQLModel


class CurrentUser(BaseModel):
    id: int = Field(None, description="User ID")

    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)
