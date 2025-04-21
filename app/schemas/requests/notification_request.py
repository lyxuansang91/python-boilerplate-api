from pydantic import BaseModel


class NotificationCreateRequest(BaseModel):
    content: str
    short_content: str
    detail_content: str
