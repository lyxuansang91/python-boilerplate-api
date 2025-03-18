from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from datetime import timedelta

from api.deps import get_db, SessionDep, get_user_repository
from core import security
from core.config import settings
from schemas.responses import TokenResponse
from schemas.requests import LoginRequest
from repositories import UserRepository


router = APIRouter()
@router.post("/login", response_model=TokenResponse)
def login_with_email(
    session: SessionDep,
    login_request: LoginRequest,
    user_repository: UserRepository = Depends(get_user_repository),
) -> TokenResponse:
    user = user_repository.authenticate(
        email=login_request.email, password=login_request.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return TokenResponse(access_token=access_token, token_type="bearer")