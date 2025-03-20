from fastapi import APIRouter

from core.config import settings

from api.routes.v1 import v1_router

router = APIRouter()

router.include_router(v1_router, prefix=settings.API_V1_STR)

__all__ = ["router"]
