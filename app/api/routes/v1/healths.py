from fastapi import APIRouter


router = APIRouter(prefix="/health", tags=["healths"])


@router.get("/health-check/")
async def health_check() -> bool:
    return True
