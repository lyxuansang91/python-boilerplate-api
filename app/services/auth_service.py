# from core.database import Propagation, Transactional
from core import security
from core.config import settings
from core.exceptions import BadRequestException
from models import User
from pydantic import EmailStr
from repositories import UserRepository
from schemas.extras.token import Token

from services import BaseService


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
