"""
Companies router for company profiles, financials, ratios, and tearsheets.
"""

from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from src.database import DatabaseManager

router = APIRouter(prefix="/companies", tags=["Companies"])
db = DatabaseManager()


@router.get("")
def list_companies(
    sector: Optional[str] = None,
    market_cap_category: Optional[str] = None,
    search: Optional[str] = None,
):
    """Return list of companies with id, company_name, broad_sector, sub_sector, roe_pct, roce_pct."""
    query = """
    SELECT 
        c.ticker AS id,
        c.name AS company_name,
        c.sector_name AS broad_sector,
        c.industry AS sub_sector,
        COALESCE(r.return_on_equity_pct, r.roe, 0.0) AS roe_pct,
        COALESCE(r.return_on_capital_employed_pct, 0.0) AS roce_pct
    FROM companies c
    LEFT JOIN financial_ratios r ON c.ticker = r.ticker
    AND r.year = (SELECT MAX(year) FROM financial_ratios WHERE ticker = c.ticker)
    WHERE 1=1
    """
    params = []
    if sector:
        query += " AND (c.sector_name = ? OR c.industry = ?)"
        params.extend([sector, sector])
    if search:
        query += " AND (c.ticker LIKE ? OR c.name LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    rows = db.execute_query(query, tuple(params))
    res = [dict(row) for row in rows]
    return res


@router.get("/{ticker}")
def get_company_profile(ticker: str):
    """Return full company profile: all company fields + latest year KPIs + sector data."""
    ticker_upper = ticker.upper()
    comp_rows = db.execute_query(
        "SELECT * FROM companies WHERE UPPER(ticker) = ?", (ticker_upper,)
    )
    if not comp_rows:
        raise HTTPException(
            status_code=404, detail=f"Company with ticker '{ticker}' not found"
        )

    company = dict(comp_rows[0])
    ratio_rows = db.execute_query(
        "SELECT * FROM financial_ratios WHERE UPPER(ticker) = ? ORDER BY year DESC LIMIT 1",
        (ticker_upper,),
    )
    kpis = dict(ratio_rows[0]) if ratio_rows else {}

    sector_rows = db.execute_query(
        "SELECT * FROM sectors WHERE sector_name = ?", (company.get("sector_name"),)
    )
    sector_info = dict(sector_rows[0]) if sector_rows else {}

    return {
        "company": company,
        "latest_kpis": kpis,
        "sector_info": sector_info,
    }


@router.get("/{ticker}/pl")
def get_profit_and_loss(
    ticker: str,
    from_year: Optional[int] = Query(None),
    to_year: Optional[int] = Query(None),
):
    """Return P&L history array for company."""
    ticker_upper = ticker.upper()
    comp_rows = db.execute_query(
        "SELECT ticker FROM companies WHERE UPPER(ticker) = ?", (ticker_upper,)
    )
    if not comp_rows:
        raise HTTPException(
            status_code=404, detail=f"Company with ticker '{ticker}' not found"
        )

    query = "SELECT * FROM profitandloss WHERE UPPER(ticker) = ?"
    params = [ticker_upper]
    if from_year is not None:
        query += " AND year >= ?"
        params.append(from_year)
    if to_year is not None:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year ASC"
    rows = db.execute_query(query, tuple(params))
    return [dict(row) for row in rows]


@router.get("/{ticker}/bs")
def get_balance_sheet(
    ticker: str,
    from_year: Optional[int] = Query(None),
    to_year: Optional[int] = Query(None),
):
    """Return Balance Sheet history array for company."""
    ticker_upper = ticker.upper()
    comp_rows = db.execute_query(
        "SELECT ticker FROM companies WHERE UPPER(ticker) = ?", (ticker_upper,)
    )
    if not comp_rows:
        raise HTTPException(
            status_code=404, detail=f"Company with ticker '{ticker}' not found"
        )

    query = "SELECT * FROM balancesheet WHERE UPPER(ticker) = ?"
    params = [ticker_upper]
    if from_year is not None:
        query += " AND year >= ?"
        params.append(from_year)
    if to_year is not None:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year ASC"
    rows = db.execute_query(query, tuple(params))
    return [dict(row) for row in rows]


@router.get("/{ticker}/cashflow")
def get_cash_flow(
    ticker: str,
    from_year: Optional[int] = Query(None),
    to_year: Optional[int] = Query(None),
):
    """Return Cash Flow history array for company."""
    ticker_upper = ticker.upper()
    comp_rows = db.execute_query(
        "SELECT ticker FROM companies WHERE UPPER(ticker) = ?", (ticker_upper,)
    )
    if not comp_rows:
        raise HTTPException(
            status_code=404, detail=f"Company with ticker '{ticker}' not found"
        )

    query = "SELECT * FROM cashflow WHERE UPPER(ticker) = ?"
    params = [ticker_upper]
    if from_year is not None:
        query += " AND year >= ?"
        params.append(from_year)
    if to_year is not None:
        query += " AND year <= ?"
        params.append(to_year)

    query += " ORDER BY year ASC"
    rows = db.execute_query(query, tuple(params))
    return [dict(row) for row in rows]


@router.get("/{ticker}/ratios")
def get_ratios(ticker: str, year: Optional[int] = Query(None)):
    """Return all computed KPIs per year for the company."""
    ticker_upper = ticker.upper()
    comp_rows = db.execute_query(
        "SELECT ticker FROM companies WHERE UPPER(ticker) = ?", (ticker_upper,)
    )
    if not comp_rows:
        raise HTTPException(
            status_code=404, detail=f"Company with ticker '{ticker}' not found"
        )

    query = "SELECT * FROM financial_ratios WHERE UPPER(ticker) = ?"
    params = [ticker_upper]
    if year is not None:
        query += " AND year = ?"
        params.append(year)

    query += " ORDER BY year ASC"
    rows = db.execute_query(query, tuple(params))
    return [dict(row) for row in rows]


@router.get("/{ticker}/tearsheet")
def get_tearsheet(ticker: str):
    """Return the pre-generated tearsheet PDF as binary download."""
    ticker_upper = ticker.upper()
    pdf_path = Path(f"reports/tearsheets/{ticker_upper}_tearsheet.pdf")
    if not pdf_path.is_file():
        # Fallback search
        alt_path = Path(f"reports/tearsheets/{ticker}_tearsheet.pdf")
        if alt_path.is_file():
            pdf_path = alt_path
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Tearsheet PDF for ticker '{ticker}' not found at {pdf_path}",
            )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{ticker_upper}_tearsheet.pdf",
    )
