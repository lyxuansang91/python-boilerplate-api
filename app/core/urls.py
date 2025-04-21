EDINET_BASE_URL = "https://disclosure.edinet-fsa.go.jp/api/v2"
EDINET_API_BASE_URL = "https://api.edinet-fsa.go.jp/api/v2"

DOCUMENTS_LIST_URL = f"{EDINET_BASE_URL}/documents.json"
DOCUMENT_DETAIL_URL = f"{EDINET_API_BASE_URL}/documents"

def get_document_url(doc_id: str) -> str:
    return f"{DOCUMENT_DETAIL_URL}/{doc_id}"
