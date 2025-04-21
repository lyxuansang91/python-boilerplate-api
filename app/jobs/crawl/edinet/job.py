# demo.py
import logging
import os
from datetime import datetime, timedelta

from app.core.aws.s3 import S3Client
from app.core.db import get_session
from app.jobs.crawl.edinet.edinet import get_document, get_documents_for_date_range
from app.repositories.company_repository import CompanyRepository

logger = logging.getLogger(__name__)

def get_megabanks() -> dict[str, str]:
    company_repository = CompanyRepository(session=get_session())
    companies, _ = company_repository.get_companies()
    return {company.code: company.name for company in companies}

def save_and_update_company(doc_res, company_repository: CompanyRepository,
                          company_code: str, doc_info: dict) -> None:
    """Save document to S3 and update company description"""
    try:
        # Prepare paths
        save_dir = 'data'
        os.makedirs(save_dir, exist_ok=True)

        save_name = f"{doc_info['edinet_code']}_{doc_info['filer']}_{doc_info['type']}_{doc_info['id']}.zip"
        local_path = os.path.join(save_dir, save_name)
        s3_key = f"edinet_docs/{datetime.now().strftime('%Y/%m/%d')}/{save_name}"

        # Save locally first
        with open(local_path, 'wb') as f:
            f.write(doc_res.read())

        # Upload to S3
        s3_client = S3Client()
        s3_url = s3_client.upload_file(local_path, s3_key, 'application/zip')

        # Update company description with S3 URL
        company = company_repository.get_by_code(company_code)
        if company:
            company_repository.update(
                company,
                {
                    "description": s3_url,
                    "valid_from": datetime.now()
                }
            )
            logger.info(f"Updated company {company_code} with new document URL")

        # Cleanup local file
        if os.path.exists(local_path):
            os.remove(local_path)

    except Exception as e:
        logger.error(f"Error processing document for company {company_code}: {str(e)}")
        if os.path.exists(local_path):
            os.remove(local_path)
        raise

def run():
    logger.info("Starting EDINET document crawler")
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=90)
    doc_type_codes = ["180"]  # Extraordinary Reports

    company_repository = CompanyRepository(session=get_session())
    companies, _ = company_repository.get_companies()
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
                'id': doc['docID'],
                'edinet_code': doc['edinetCode'],
                'type': doc['docTypeCode'],
                'filer': doc['filerName']
            }

            doc_res = get_document(doc_info['id'])
            save_and_update_company(
                doc_res,
                company_repository,
                doc['edinetCode'],
                doc_info
            )
            results.append(doc_info)

        except Exception as e:
            logger.error(f"Error processing document {doc['docID']}: {str(e)}")
            continue

    logger.info(f"Successfully processed {len(results)} documents")
    return results


