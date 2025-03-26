from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi.security import HTTPBearer
from passlib.context import CryptContext

from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

bearer_security = HTTPBearer(auto_error=False)


def create_token(
    subject: str | Any, expires_delta: int, token_type: str | Any = "access_token"
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
    to_encode = {"exp": expire, "sub": str(subject), "type": token_type}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_reset_token(user_id: int) -> str:
    return create_token(
        subject=user_id,
        expires_delta=settings.RESET_TOKEN_EXPIRE_MINUTES,
        token_type="reset",
    )


def get_sub_from_token(token: str) -> Any:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload["sub"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception):
        return None
