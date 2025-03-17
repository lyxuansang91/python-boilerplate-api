from enum import Enum
from uuid import uuid4

from core.database import Base
from core.database.mixins import TimestampMixin
from sqlalchemy import BigInteger, Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID


class UserPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)
