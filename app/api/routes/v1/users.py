
from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter()


@router.get("/")
def read_users():
    """
    Retrieve a list of users.

    Returns:
    list: A list of dictionaries, each containing the username of a user.
    """
    return [{"username": "Rick"}, {"username": "Morty"}]

