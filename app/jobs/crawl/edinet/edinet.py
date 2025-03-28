# edinet_tools.py
import datetime
import json
import os
import urllib.parse
import urllib.request

from app.core.config import settings


# API interaction functions
def fetch_documents_list(date: str | datetime.date, type: int = 2) -> dict:
    """Retrieve disclosure documents from EDINET API for a specified date."""
    if isinstance(date, str):
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date string. Use format 'YYYY-MM-DD'")
        date_str = date
    elif isinstance(date, datetime.date):
        date_str = date.strftime("%Y-%m-%d")
    else:
        raise TypeError("Date must be 'YYYY-MM-DD' or datetime.date")
    url = "https://disclosure.edinet-fsa.go.jp/api/v2/documents.json"
    params = {
        "date": date_str,
        "type": type,  # '1' is metadata only; '2' is metadata and results
        "Subscription-Key": settings.EDINET_API_KEY,
    }
    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"

    with urllib.request.urlopen(full_url) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_document(doc_id: str) -> urllib.request.urlopen:
    """Retrieve a specific document from EDINET API."""
    url = f"https://api.edinet-fsa.go.jp/api/v2/documents/{doc_id}"
    params = {
        "type": 5,  # '5' for CSV
        "Subscription-Key": settings.EDINET_API_KEY,
    }
    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"
    return urllib.request.urlopen(full_url)


def save_document_content(doc_res: urllib.request.urlopen, output_path: str) -> None:
    """Save the document content to file."""
    with open(output_path, "wb") as file_out:
        file_out.write(doc_res.read())


def download_documents(docs: list[dict], download_dir: str = "./downloads") -> None:
    """
    Download all documents in the provided list.
    """
    os.makedirs(download_dir, exist_ok=True)

    for i, doc in enumerate(docs, 1):
        doc_id = doc["docID"]
        doc_type_code = doc["docTypeCode"]
        filer = doc["filerName"]

        save_name = f"{doc_id}-{doc_type_code}-{filer}.zip"
        output_path = os.path.join(download_dir, save_name)

        print(f"Downloading {i}/{len(docs)}: `{save_name}`")

        if not os.path.exists(output_path):
            try:
                # make GET request to `documents/{docID}` endpoint
                doc_res = fetch_document(doc_id)
                save_document_content(doc_res, output_path)
            except Exception as e:
                print(f"Error downloading {save_name}: {str(e)}")
        else:
            # print(f"File already exists: {save_name}")
            pass
    print(f"\nDownloads complete. Files saved to: `{download_dir}`\n")


# Document filtering and processing


def filter_documents(
    docs: list[dict],
    edinet_codes: list[str] | str = [],  # noqa: B006
    doc_type_codes: list[str] | str = [],  # noqa: B006
    excluded_doc_type_codes: list[str] | str = [],  # noqa: B006
    require_sec_code: bool = True,
) -> list[dict]:
    """Filter list of documents by EDINET codes and document type codes."""
    if isinstance(edinet_codes, str):
        edinet_codes = [edinet_codes]
    if isinstance(doc_type_codes, str):
        doc_type_codes = [doc_type_codes]
    if isinstance(excluded_doc_type_codes, str):
        excluded_doc_type_codes = [excluded_doc_type_codes]

    return [
        doc
        for doc in docs
        if (not edinet_codes or doc["edinetCode"] in edinet_codes)
        and (not doc_type_codes or doc["docTypeCode"] in doc_type_codes)
        and (doc["docTypeCode"] not in excluded_doc_type_codes)
        and (not require_sec_code or doc.get("secCode") is not None)
    ]


def get_documents_for_date_range(
    start_date: datetime.date,
    end_date: datetime.date,
    edinet_codes: list[str],
    doc_type_codes: list[str],
    excluded_doc_type_codes: list[str],
    require_sec_code: bool = True,
) -> list[dict]:
    """Retrieve documents for a date range."""
    if edinet_codes is None:
        edinet_codes = []
    matching_docs = []
    current_date = start_date
    while current_date <= end_date:
        docs_res = fetch_documents_list(date=current_date)
        if docs_res["results"]:
            filtered_docs = filter_documents(
                docs_res["results"],
                edinet_codes,
                doc_type_codes,
                excluded_doc_type_codes,
                require_sec_code,
            )

            matching_docs.extend(filtered_docs)
        current_date += datetime.timedelta(days=1)
    return matching_docs


def get_document(doc_id: str) -> urllib.request.urlopen:
    """Retrieve a specific document from EDINET API."""
    url = f"https://api.edinet-fsa.go.jp/api/v2/documents/{doc_id}"
    params = {
        "type": 5,  # '5' for CSV
        "Subscription-Key": settings.EDINET_API_KEY,
    }
    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"
    return urllib.request.urlopen(full_url)


def save_document(doc_res: urllib.request.urlopen, output_path: str) -> None:
    """Save the document content to file."""
    with open(output_path, "wb") as file_out:
        file_out.write(doc_res.read())
    print(f"Saved: {output_path}")
