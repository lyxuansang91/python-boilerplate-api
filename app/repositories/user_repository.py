from typing import Optional
from models import User
from .base_repository import BaseRepository
from core import security
class UserRepository(BaseRepository[User]):

    def __init__(self, session):
        super().__init__(model=User, session=session)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.session.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not security.verify_password(password, user.password):
            return None
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> Optional[User]:
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