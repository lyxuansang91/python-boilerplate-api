import logging
from datetime import datetime, timedelta

from app.core.aws.s3 import S3Client
from app.core.db import get_session
from app.jobs.crawl.edinet.edinet import get_document, get_documents_for_date_range
from app.models.company import Company
from app.models.report import DOCUMENT_TYPE, REPORT_TYPE, Report
from app.repositories.company_repository import CompanyRepository
from app.repositories.report_repository import ReportRepository

logger = logging.getLogger(__name__)
session = next(get_session())

class EdinetCrawler:
    def __init__(self):
        self.company_repository = CompanyRepository(session=session, model=Company)
        self.report_repository = ReportRepository(session=session, model=Report)
        self.s3_client = S3Client()

    def get_megabanks(self) -> dict[str, str]:
        companies, _ = self.company_repository.get_companies()
        return {company.code: company.name for company in companies}

    def save_and_update_report_company(self, doc_id, company_code: str, doc_info: dict, start_date, end_date) -> None:
        """Save document to S3 and update company description"""
        try:
            doc_res = get_document(doc_id)
            save_name = f"{doc_info['edinet_code']}_{doc_info['filer']}_{doc_info['doc_type']}_{doc_info['id']}.zip"
            s3_key = f"edinet_docs/{datetime.now().strftime('%Y/%m/%d')}/{save_name}"

            s3_url = self.s3_client.upload_file_with_response(doc_res, s3_key, 'application/zip')

            # Cập nhật thông tin công ty
            company = self.company_repository.get_by_code(company_code)
            if company:
                self.company_repository.update(
                    company,
                    {
                        "description": s3_url,
                        "valid_from": datetime.now()
                    }
                )
                logger.info(f"Updated company {company_code} with new document URL")

                # Thêm dữ liệu vào bảng 'reports'
                self.report_repository.create({
                    "company_id": company.id,
                    "code": company_code,
                    "report_type": REPORT_TYPE.REPORT,
                    "submitted_document": doc_info['filer'],
                    "submission_time": doc_info['submit_date_time'],
                    "submitter": doc_info.get('filer', ''),
                    "document_type": DOCUMENT_TYPE.ZIP,
                    "remark": "Document uploaded successfully",
                    "file_path": s3_url,
                    "raw_report_content": None,
                    "valid_from": start_date,
                    "valid_to": end_date,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                })

        except Exception as e:
            logger.error(f"Error processing document for company {company_code}: {str(e)}")
            raise

    def run(self):
        logger.info("Starting EDINET document crawler")
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=400)
        doc_type_codes = ["120","130","140","150","160","170"]  # Extraordinary Reports

        companies, _ = self.company_repository.get_companies()
        company_codes = {company.code: company.name for company in companies}

        docs = get_documents_for_date_range(
            start_date,
            end_date,
            list(company_codes.keys()),
            doc_type_codes
        )

        if not docs:
            logger.info("No documents found")
            return []

        results = []
        for doc in docs:
            try:
                doc_info = {
                    'seq_number': doc.get('seqNumber'),
                    'id': doc.get('docID'),
                    'edinet_code': doc.get('edinetCode'),
                    'sec_code': doc.get('secCode'),
                    'jcn': doc.get('JCN'),
                    'filer': doc.get('filerName'),
                    'period_start': doc.get('periodStart'),
                    'period_end': doc.get('periodEnd'),
                    'submit_date_time': doc.get('submitDateTime'),
                    'doc_description': doc.get('docDescription'),
                    'doc_type': doc.get('docTypeCode'),
                    'pdf_flag': doc.get('pdfFlag'),
                    'csv_flag': doc.get('csvFlag'),
                    'attach_doc_flag': doc.get('attachDocFlag'),
                    'fund_code': doc.get('fundCode'),
                    'ordinance_code': doc.get('ordinanceCode'),
                    'form_code': doc.get('formCode'),
                    'issuer_edinet_code': doc.get('issuerEdinetCode'),
                    'subject_edinet_code': doc.get('subjectEdinetCode'),
                    'subsidiary_edinet_code': doc.get('subsidiaryEdinetCode'),
                    'current_report_reason': doc.get('currentReportReason'),
                    'parent_doc_id': doc.get('parentDocID'),
                    'ope_date_time': doc.get('opeDateTime'),
                    'withdrawal_status': doc.get('withdrawalStatus'),
                    'doc_info_edit_status': doc.get('docInfoEditStatus'),
                    'disclosure_status': doc.get('disclosureStatus'),
                    'xbrl_flag': doc.get('xbrlFlag'),
                    'legal_status': doc.get('legalStatus'),
                }


                self.save_and_update_report_company(
                    doc_info['id'],
                    doc['edinetCode'],
                    doc_info,
                    start_date=start_date,
                    end_date=end_date,
                )
                results.append(doc_info)

            except Exception as e:
                logger.error(f"Error processing document {doc['docID']}: {str(e)}")
                continue

        logger.info(f"Successfully processed {len(results)} documents")
        return results
