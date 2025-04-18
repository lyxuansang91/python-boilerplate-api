from typing import Any

from app.models import Notification
from app.repositories import NotificationRepository

from .base_service import BaseService


class NotificationService(BaseService[Notification]):
    def __init__(self, notification_repository: NotificationRepository):
        super().__init__(model=Notification, repository=notification_repository)
        self.notification_repository = notification_repository

    def get_notifications(
        self, skip: int = 0, limit: int = 10, search: str | None = None
    ) -> tuple[list[Notification], int]:
        return self.notification_repository.get_notifications(
            skip=skip, limit=limit, search=search
        )

    def create_notification(self, notification: dict[str, Any]) -> Notification:
        return self.notification_repository.create(attributes=notification)
