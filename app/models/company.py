from sqlalchemy import Column, Integer, String, DateTime
from . import Base
from .timestamp import TimestampMixin


class Company(Base, TimestampMixin):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    description = Column(String)
    valid_from = Column(DateTime)
    valid_to = Column(DateTime)

    def __repr__(self):
        return f"<Company(name={self.name}, code={self.code})>"
