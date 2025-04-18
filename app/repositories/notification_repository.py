from typing import Optional, Tuple

from app.models import Notification
from .base_repository import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    def get_by_id(self, notification_id: int) -> Optional[Notification]:
        return (
            self.session.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )

    def get_notifications(
        self, skip: int = 0, limit: int = 10, search: Optional[str] = None
    ) -> Tuple[list[Notification], int]:
        query = self.session.query(Notification)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                Notification.content.ilike(search_pattern)
                | Notification.short_content.ilike(search_pattern)
            )

        count = query.count()
        notifications = (
            query.order_by(Notification.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return notifications, count
