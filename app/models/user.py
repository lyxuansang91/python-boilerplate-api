from enum import Enum

from sqlalchemy import BigInteger, Boolean, Column, String

from . import Base
from .timestamp import TimestampMixin


class UserPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    hash_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default=UserRole.USER.value)
    is_active = Column(Boolean, default=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)

    @property
    def user_role(self) -> UserRole:
        return UserRole(self.role)
