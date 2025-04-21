from datetime import datetime

from pydantic import BaseModel


class NotificationResponse(BaseModel):
    id: int
    content: str
    short_content: str
    detail_content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]
    total: int
    page: int
    size: int
    pages: int
