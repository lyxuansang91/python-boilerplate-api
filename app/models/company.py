from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from . import Base
from .timestamp import TimestampMixin


class Company(Base, TimestampMixin):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    description = Column(String)
    valid_from = Column(DateTime(timezone=True))
    valid_to = Column(DateTime(timezone=True))
    def __repr__(self):
        return f"<Company(name={self.name}, code={self.code})>"
