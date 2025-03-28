
from app.models.report import Report

from .base_repository import BaseRepository


class ReportRepository(BaseRepository[Report]):
    def get_reports_by_company_id(self, id: int | None = None, skip: int = 0, limit: int = 10) -> tuple[
        list[type[Report]], int]:
        query = self.session.query(Report)

        if id:
            query = query.filter(
                Report.id == id
            )

        count_reports = query.count()
        reports = query.offset(skip).limit(limit).all()

        return reports, count_reports
