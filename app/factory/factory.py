from functools import partial

from deps import SessionDep
from models import User
from repositories import UserRepository
from services import AuthService, UserService


class Factory:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application.
    """

    # Repositories
    user_repository = partial(UserRepository, User)

    def get_user_service(self, session=SessionDep):
        return UserService(user_repository=self.user_repository(session=session))

    def get_auth_service(self, session=SessionDep):
        return AuthService(user_repository=self.user_repository(session=session))
