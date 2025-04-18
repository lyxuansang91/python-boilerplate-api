from sqlalchemy import Column, Integer, String, Text

from . import Base
from .timestamp import TimestampMixin


class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255), nullable=False)
    short_content = Column(String(100), nullable=False)
    detail_content = Column(Text, nullable=True)
