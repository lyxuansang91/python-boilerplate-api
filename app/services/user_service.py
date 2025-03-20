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
