from collections.abc import Generator
from typing import Annotated

import jwt
from core import security
from core.config import settings
from core.db import engine
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from models import User
from pydantic import ValidationError
from repositories import UserRepository
from sqlalchemy.orm import Session


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


def get_user_repository(
    session: Session = Depends(get_db),
) -> Generator[UserRepository, None, None]:
    return UserRepository(session)


def get_current_user(session: SessionDep, token: str) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        user = session.get(User, payload.get("sub"))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
