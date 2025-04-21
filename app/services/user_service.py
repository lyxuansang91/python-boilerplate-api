from typing import Any

from app.core.config import settings
from app.core.email import send_email
from app.core.security import get_password_hash, get_sub_from_token, verify_password
from app.models import User
from app.repositories import UserRepository

from . import BaseService


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

    def update_password(self, user: User, old_password: str, new_password: str) -> None:
        if not verify_password(old_password, user.hash_password):
            raise Exception("Invalid old password")
        user.hash_password = get_password_hash(new_password)
        self.user_repository.update(user, {"hash_password": user.hash_password})

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
        reset_url = (
            f"https://{settings.FRONT_END_URL}/reset-password?token={reset_token}"
        )
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
        if sub:
            user = self.user_repository.get_by_id(int(sub))
            if user:
                self.update_user(user, {"password": new_password})
            else:
                raise Exception("Invalid token")
        else:
            raise Exception("Invalid token")

    def verify_reset_token(self, token: str) -> bool:
        sub = get_sub_from_token(token)
        if sub is None:
            return False

        user = self.user_repository.get_by_id(int(sub))
        return True if user else False
