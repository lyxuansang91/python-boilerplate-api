from pydantic import SQLModel


class Token(SQLModel):
    access_token: str
    refresh_token: str
