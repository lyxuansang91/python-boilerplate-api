from fastapi import APIRouter, Depends, Query

from app.deps import get_current_user
from app.factory import factory_instance
from app.models import User
from app.schemas.responses import NotificationResponse, PaginatedResponse
from app.services import NotificationService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[NotificationResponse])
def list_notifications(
    search: str | None = Query(None, description="Search term for notifications"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    current_user: User = Depends(get_current_user),  # noqa
    notification_service: NotificationService = Depends(
        factory_instance.get_notification_service
    ),
) -> PaginatedResponse[NotificationResponse]:
    """
    Retrieve a paginated list of notifications.

    Parameters:
    - search: Optional search term to filter notifications
    - page: Page number (1-based)
    - limit: Number of items per page
    - current_user: The currently authenticated user
    - notification_service: The notification service instance

    Returns:
    - NotificationListResponse: Paginated list of notifications
    """
    skip = (page - 1) * limit
    notifications, total = notification_service.get_notifications(
        skip=skip, limit=limit, search=search
    )

    return PaginatedResponse[NotificationResponse](
        items=notifications,
        total=total,
        page=page,
        size=len(notifications),
        pages=total // limit if total % limit == 0 else total // limit + 1,
    )
