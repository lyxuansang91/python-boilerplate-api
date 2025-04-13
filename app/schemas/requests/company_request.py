from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class CompanyInDB(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Company(CompanyInDB):
    pass 