from app.models.company import Company
from sqlalchemy.orm import Session
from typing import Optional, Tuple, List

class CompanyRepository:
    def __init__(self, session: Session):
        self.session = session
        self.model_class = Company

    def get_by_id(self, company_id: int) -> Optional[Company]:
        return self.session.query(Company).filter(Company.id == company_id).first()

    def get_by_code(self, code: str) -> Optional[Company]:
        return self.session.query(Company).filter(Company.code == code).first()

    def create_company(self, company_data: dict) -> Company:
        company = Company(**company_data)
        self.session.add(company)
        self.session.commit()
        self.session.refresh(company)
        return company

    def update(self, company: Company, data: dict) -> Company:
        """Update company with new data"""
        for key, value in data.items():
            setattr(company, key, value)
        self.session.add(company)
        self.session.commit()
        self.session.refresh(company)
        return company

    def get_companies(self, search: Optional[str] = None, skip: int = 0, limit: int = 10) -> Tuple[List[Company], int]:
        query = self.session.query(Company)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                Company.name.ilike(search_pattern) |
                Company.code.ilike(search_pattern)
            )

        count_companies = query.count()
        companies = query.offset(skip).limit(limit).all()

        return companies, count_companies