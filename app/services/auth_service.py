# from core.database import Propagation, Transactional
from pydantic import EmailStr

from app.core import security
from app.core.config import settings
from app.core.exceptions import BadRequestException
from app.models import User
from app.repositories import UserRepository
from app.schemas.extras.token import Token

from . import BaseService


class AuthService(BaseService[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    def register(self, email: EmailStr, password: str) -> User:
        # Check if user exists with email
        user = self.user_repository.get_by_email(email)

        if user:
            raise BadRequestException("User already exists with this email")

        hash_password = security.get_password_hash(password=password)

        return self.user_repository.create(
            {
                "email": email,
                "hash_password": hash_password,
            }
        )

    def login(self, email: EmailStr, password: str) -> Token:
        user = self.user_repository.get_by_email(email)

        if not user:
            raise BadRequestException("Invalid credentials")

        if not security.verify_password(password, user.hash_password):
            raise BadRequestException("Invalid credentials")

        return Token(
            access_token=security.create_token(
                subject=user.id,
                expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
                token_type="access_token",
            ),
            refresh_token=security.create_token(
                subject=user.id,
                expires_delta=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
                token_type="refresh_token",
            ),
        )

    def refresh_token(self, refresh_token: str) -> Token:
        """Generate a new access token using refresh token"""
        try:
            # Verify the refresh token
            user_id = security.get_sub_from_token(refresh_token)
            if not user_id:
                raise BadRequestException("Invalid refresh token")

            # Get user from database
            user = self.user_repository.get_by_id(user_id)
            if not user:
                raise BadRequestException("User not found")

            # Generate new tokens
            return Token(
                access_token=security.create_token(
                    subject=user.id,
                    expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
                    token_type="access_token",
                ),
                refresh_token=security.create_token(
                    subject=user.id,
                    expires_delta=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
                    token_type="refresh_token",
                ),
            )
        except Exception as e:
            raise BadRequestException(str(e))
