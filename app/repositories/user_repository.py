from app.core import security
from app.models import User

from .base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def authenticate(self, email: str, password: str) -> User | None:
        user = self.session.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not security.verify_password(password, user.password):
            return None
        return user

    def get_by_email(self, email: str) -> User | None:
        return self.session.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.session.query(User).filter(User.id == user_id).first()

    def create_user(self, user_data: dict) -> User:
        user_data["hash_password"] = security.get_password_hash(user_data["password"])
        del user_data["password"]
        return self.create(user_data)

    def get_users(self, search: str | None, skip: int = 0, limit: int = 10):
        count_users = self._count(self._query(join_=None))
        users = self.get_all(skip=skip, limit=limit)

    def create_reset_token(self, user: User) -> str | None:
        return security.create_reset_token(user.id)

    def get_by_reset_token(self, token: str) -> User | None:
        return self.session.query(User).filter(User.reset_token == token).first()
