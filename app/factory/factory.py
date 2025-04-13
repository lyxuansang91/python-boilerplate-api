from functools import partial

from fastapi import Depends

from app.deps import get_db
from app.models import User, Company
from app.repositories import UserRepository, CompanyRepository
from app.services import AuthService, UserService, CompanyService


class Factory:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application.
    """

    # Repositories
    user_repository = partial(UserRepository, User)
    company_repository = partial(CompanyRepository, Company)

    def get_user_service(self, session=Depends(get_db)):
        return UserService(user_repository=Factory.user_repository(session=session))

    def get_auth_service(self, session=Depends(get_db)):
        return AuthService(user_repository=Factory.user_repository(session=session))

    def get_company_service(self, session=Depends(get_db)):
        return CompanyService(company_repository=Factory.company_repository(session=session))


factory_instance = Factory()