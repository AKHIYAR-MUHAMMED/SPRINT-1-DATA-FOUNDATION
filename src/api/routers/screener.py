"""
Screener router for multi-factor stock filtering.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from src.database import DatabaseManager

router = APIRouter(prefix="/screener", tags=["Screener"])
db = DatabaseManager()


@router.get("")
def screen_companies(
    min_roe: Optional[float] = Query(None),
    max_de: Optional[float] = Query(None),
    min_fcf: Optional[float] = Query(None),
    sector: Optional[str] = Query(None),
    min_rev_cagr_5yr: Optional[float] = Query(None),
    min_pat_cagr_5yr: Optional[float] = Query(None),
    max_pe: Optional[float] = Query(None),
):
    """Filter companies based on financial criteria and return ranked results."""
    # Validation checks for HTTP 400
    if min_roe is not None and (min_roe < -500 or min_roe > 1000):
        raise HTTPException(
            status_code=400, detail="Invalid min_roe parameter value"
        )
    if max_de is not None and max_de < 0:
        raise HTTPException(status_code=400, detail="max_de cannot be negative")
    if max_pe is not None and max_pe < 0:
        raise HTTPException(status_code=400, detail="max_pe cannot be negative")

    query = """
    SELECT 
        c.ticker AS company_id,
        c.name AS company_name,
        c.sector_name AS broad_sector,
        COALESCE(r.return_on_equity_pct, r.roe, 0.0) AS return_on_equity_pct,
        COALESCE(r.debt_to_equity, 0.0) AS debt_to_equity,
        COALESCE(r.free_cash_flow_cr, 0.0) AS free_cash_flow_cr,
        COALESCE(r.revenue_cagr_5yr, 0.0) AS revenue_cagr_5yr,
        COALESCE(r.pat_cagr_5yr, 0.0) AS pat_cagr_5yr,
        COALESCE(r.pe_ratio, 0.0) AS pe_ratio,
        COALESCE(r.composite_quality_score, 50.0) AS quality_score
    FROM companies c
    LEFT JOIN financial_ratios r ON c.ticker = r.ticker
    AND r.year = (SELECT MAX(year) FROM financial_ratios WHERE ticker = c.ticker)
    WHERE 1=1
    """
    params = []

    if sector:
        query += " AND (c.sector_name = ? OR c.industry = ?)"
        params.extend([sector, sector])
    if min_roe is not None:
        query += " AND COALESCE(r.return_on_equity_pct, r.roe) >= ?"
        params.append(min_roe)
    if max_de is not None:
        query += " AND COALESCE(r.debt_to_equity, 0) <= ?"
        params.append(max_de)
    if min_fcf is not None:
        query += " AND COALESCE(r.free_cash_flow_cr, 0) >= ?"
        params.append(min_fcf)
    if min_rev_cagr_5yr is not None:
        query += " AND COALESCE(r.revenue_cagr_5yr, 0) >= ?"
        params.append(min_rev_cagr_5yr)
    if min_pat_cagr_5yr is not None:
        query += " AND COALESCE(r.pat_cagr_5yr, 0) >= ?"
        params.append(min_pat_cagr_5yr)
    if max_pe is not None:
        query += " AND COALESCE(r.pe_ratio, 9999) <= ?"
        params.append(max_pe)

    query += " ORDER BY quality_score DESC, return_on_equity_pct DESC"
    rows = db.execute_query(query, tuple(params))
    return [dict(row) for row in rows]
