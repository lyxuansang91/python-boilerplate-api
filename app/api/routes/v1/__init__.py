from fastapi import APIRouter

from .auth import router as auth_router
from .healths import router as healths_router
from .users import router as users_router
from .companies import router as companies_router

v1_router = APIRouter()

v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v1_router.include_router(healths_router, prefix="/healths", tags=["healths"])
v1_router.include_router(users_router, prefix="/users", tags=["users"])
v1_router.include_router(companies_router, prefix="/companies", tags=["companies"])
