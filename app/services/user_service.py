from typing import Any

from core.email import send_email
from core.security import get_password_hash, get_sub_from_token
from core.config import settings
from models import User
from repositories import UserRepository

from services import BaseService


class UserService(BaseService[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    def get_by_username(self, username: str) -> User:
        return self.user_repository.get_by_username(username)

    def get_by_email(self, email: str) -> User:
        return self.user_repository.get_by_email(email)

    def authenticate(self, email: str, password: str) -> User:
        return self.user_repository.authenticate(email, password)

    def update_user(self, user: User, updated_info: dict[Any, str]) -> User:
        password = updated_info.get("password")
        if password:
            updated_info["hash_password"] = get_password_hash(password)
        return self.user_repository.update(user, updated_info)

    def create_user(self, user_data: dict[Any, str]) -> User:
        user_data["hash_password"] = get_password_hash(user_data["password"])
        del user_data["password"]
        return self.user_repository.create(user_data)

    def get_users(
        self, search: str | None, skip: int = 0, limit: int = 10
    ) -> tuple[list[User], int]:
        query = self.user_repository._query()

        if search:
            search_filter = f"%{search}%"
            query = query.filter(User.email.ilike(search_filter))
        count = self.user_repository._count(query=query)
        users = self.user_repository._all(query.offset(skip).limit(limit))

        return users, count

    def send_forgot_password_email(self, user: User, reset_token: str) -> None:
        subject = "Password Reset Request"
        reset_url = f"https://{settings.FRONT_END_URL}/reset-password?token={reset_token}"
        body = f"""
        Hi {user.email},

        You requested to reset your password. Click the link below to reset it:
        {reset_url}

        If you did not request this, please ignore this email.

        Thanks,
        Your Team
        """
        send_email(to=user.email, subject=subject, body=body)

    def trigger_password_reset(self, user: User) -> None:
        reset_token = self.user_repository.create_reset_token(user)
        self.send_forgot_password_email(user, reset_token)

    def send_email(self, email: str, subject: str, body: str) -> None:
        # Send email using an email service
        send_email(to=email, subject=subject, body=body)

    def reset_password(self, token: str, new_password: str) -> None:
        sub = get_sub_from_token(token)
        user = self.user_repository.get_by_id(int(sub))
        if not user:
            raise Exception("Invalid token")
        self.update_user(user, {"password": new_password})
