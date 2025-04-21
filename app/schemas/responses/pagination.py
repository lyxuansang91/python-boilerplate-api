from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound=object)

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int | None
    pages: int
