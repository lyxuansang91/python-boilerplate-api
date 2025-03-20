from core import security
from models import User

from .base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session):
        super().__init__(model=User, session=session)

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.session.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not security.verify_password(password, user.password):
            return None
        return user

    def get_by_email(self, email: str) -> User | None:
        return self.session.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> User | None:
        return self.session.query(User).filter(User.username == username).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.session.query(User).filter(User.id == user_id).first()

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
