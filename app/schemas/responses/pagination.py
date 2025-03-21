from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel

T = TypeVar('T', bound=object)

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int | None
    pages: int