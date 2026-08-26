"""
Documents router for company annual reports and document links.
"""

from fastapi import APIRouter, HTTPException
from src.database import DatabaseManager

router = APIRouter(prefix="/companies", tags=["Documents"])
db = DatabaseManager()


@router.get("/{ticker}/documents")
def get_company_documents(ticker: str):
    """Return annual report links with is_url_valid boolean flag for each."""
    ticker_upper = ticker.upper()
    comp_rows = db.execute_query(
        "SELECT ticker, name, website FROM companies WHERE UPPER(ticker) = ?",
        (ticker_upper,),
    )
    if not comp_rows:
        raise HTTPException(
            status_code=404, detail=f"Company with ticker '{ticker}' not found"
        )

    doc_rows = db.execute_query(
        "SELECT * FROM documents WHERE UPPER(ticker) = ?", (ticker_upper,)
    )

    documents = []
    if doc_rows:
        for r in doc_rows:
            d = dict(r)
            url = d.get("document_url") or d.get("file_path") or ""
            is_valid = bool(url and (url.startswith("http") or url.endswith(".pdf")))
            documents.append(
                {
                    "id": d.get("id"),
                    "ticker": d.get("ticker"),
                    "title": d.get("title") or f"Annual Report FY25 {ticker_upper}",
                    "document_url": url,
                    "is_url_valid": is_valid,
                }
            )
    else:
        # Fallback default document entry if none in db table
        company = dict(comp_rows[0])
        web = company.get("website", "")
        documents.append(
            {
                "id": 1,
                "ticker": ticker_upper,
                "title": f"Annual Report FY25 {ticker_upper}",
                "document_url": (
                    f"{web}/annual_report_fy25.pdf" if web else f"/reports/FY25_{ticker_upper}.pdf"
                ),
                "is_url_valid": bool(web and web.startswith("http")),
            }
        )

    return documents
