from typing import Any

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]