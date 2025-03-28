from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import engine
from app.core.security import bearer_security
from app.models import User, UserRole
from app.repositories import UserRepository


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(model=User, session=session)


def get_current_user(
        token: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_security)],
        user_repository: UserRepository = Depends(get_user_repository),
        ) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token or not token.credentials:
        raise credentials_exception

    try:
        payload = jwt.decode(
            token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: int = int(payload.get('sub'))
        if user_id is None:
            raise credentials_exception
        user = user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user
    except (InvalidTokenError, ValidationError):
        raise credentials_exception


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_admin(current_user: CurrentUser) -> User:
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
