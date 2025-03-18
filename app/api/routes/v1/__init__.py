from fastapi import APIRouter

from .users import router as users_router
from .login import router as login_router
from .healths import router as healths_router

v1_router = APIRouter()
v1_router.include_router(users_router, prefix="/users", tags=["users"])
v1_router.include_router(login_router, prefix="/auth", tags=["auth"])
v1_router.include_router(healths_router, prefix="/healths", tags=["healths"])