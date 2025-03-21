from typing import Any
from fastapi import APIRouter


router = APIRouter()


@router.get("/liveness")
def get_liveness() -> dict[Any, str]:
    return {"status": "UP"}


@router.get("/readiness")
def get_readiness() -> dict[Any, str]:
    return {"status": "UP"}