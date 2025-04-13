from typing import Any
from app.models import Company
from app.repositories import CompanyRepository

from .base_service import BaseService


class CompanyService(BaseService[Company]):
    def __init__(self, company_repository: CompanyRepository):
        super().__init__(model=Company, repository=company_repository)
        self.company_repository = company_repository

    def get_companies(self, skip: int = 0, limit: int = 100) -> tuple[list[Company], int]:
        return self.company_repository.get_companies(skip=skip, limit=limit)
    
    def get_companies_by_code(self, code: str | None = None, skip: int = 0, limit: int = 100) -> tuple[list[Company], int]:
        return self.company_repository.get_companies_by_code(code=code, skip=skip, limit=limit)
    
    def create_company(self, company: dict[str, Any]) -> Company:
        return self.company_repository.create(attributes=company)
    
    
