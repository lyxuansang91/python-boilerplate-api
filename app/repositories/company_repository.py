

from app.models.company import Company

from .base_repository import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    def get_by_id(self, company_id: int) -> Company | None:
        return self.session.query(Company).filter(Company.id == company_id).first()

    def get_by_code(self, code: str) -> Company | None:
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

    def get_companies(self, search: str | None = None, skip: int = 0, limit: int = 10) -> tuple[list[Company], int]:
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
