from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, Column, DateTime, Integer, String

from . import Base


class REPORT_TYPE(Enum):
    ANNUAL = "annual"
    REPORT = "report"
    POSSESSION_REPORT = "possession report"
    EXTRAORDINARY_REPORT = "extraordinary report"
    OTHER = "other"

class DOCUMENT_TYPE(Enum):
    PDF = "pdf"
    CSV = "csv"
    ZIP = "zip"

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(String, nullable=False)
    code = Column(String, nullable=False)
    report_type = Column(String, nullable=False, comment="Annual report, Possession report, Extraordinary report, Other")
    submitted_document = Column(String, nullable=True)
    submission_time = Column(DateTime, nullable=True)
    submitter = Column(String, nullable=True)
    document_type = Column(String, nullable=False, comment="PDF, CSV")
    remark = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    raw_report_content = Column(JSON, nullable=True)
    valid_from = Column(DateTime, nullable=True)
    valid_to = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
