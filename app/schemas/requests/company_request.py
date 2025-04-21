from datetime import datetime

from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    code: str
    description: str | None = None
    valid_from: datetime | None = None
    valid_to: datetime | None = None


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
