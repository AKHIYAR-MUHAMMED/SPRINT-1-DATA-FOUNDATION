"""
Sectors router for sector-level metrics and company aggregation.
"""

import pandas as pd
from fastapi import APIRouter, HTTPException
from src.database import DatabaseManager

router = APIRouter(prefix="/sectors", tags=["Sectors"])
db = DatabaseManager()


@router.get("")
def list_sectors():
    """Return all 11 sectors with company_count, median_roe, median_pe, median_de."""
    query = """
    SELECT 
        c.sector_name,
        COALESCE(r.return_on_equity_pct, r.roe) AS roe,
        r.pe_ratio,
        r.debt_to_equity
    FROM companies c
    LEFT JOIN financial_ratios r ON c.ticker = r.ticker
    AND r.year = (SELECT MAX(year) FROM financial_ratios WHERE ticker = c.ticker)
    """
    rows = db.execute_query(query)
    df = pd.DataFrame([dict(r) for r in rows])
    if df.empty:
        return []

    sectors_summary = []
    for sector, group in df.groupby("sector_name"):
        if pd.isna(sector) or not sector:
            continue
        sectors_summary.append(
            {
                "sector_name": sector,
                "company_count": int(len(group)),
                "median_roe": (
                    round(float(group["roe"].median()), 2)
                    if not group["roe"].dropna().empty
                    else 0.0
                ),
                "median_pe": (
                    round(float(group["pe_ratio"].median()), 2)
                    if not group["pe_ratio"].dropna().empty
                    else 0.0
                ),
                "median_de": (
                    round(float(group["debt_to_equity"].median()), 2)
                    if not group["debt_to_equity"].dropna().empty
                    else 0.0
                ),
            }
        )
    return sectors_summary


@router.get("/{sector}/companies")
def get_sector_companies(sector: str):
    """Return all companies in a sector with latest year KPIs. HTTP 404 if sector unknown."""
    query = """
    SELECT 
        c.ticker AS company_id,
        c.name AS company_name,
        c.sector_name,
        c.industry AS sub_sector,
        COALESCE(r.return_on_equity_pct, r.roe, 0.0) AS roe_pct,
        COALESCE(r.return_on_capital_employed_pct, 0.0) AS roce_pct,
        COALESCE(r.pe_ratio, 0.0) AS pe_ratio,
        COALESCE(r.debt_to_equity, 0.0) AS debt_to_equity,
        COALESCE(r.revenue_cagr_5yr, 0.0) AS revenue_cagr_5yr
    FROM companies c
    LEFT JOIN financial_ratios r ON c.ticker = r.ticker
    AND r.year = (SELECT MAX(year) FROM financial_ratios WHERE ticker = c.ticker)
    WHERE UPPER(c.sector_name) = UPPER(?) OR UPPER(c.industry) = UPPER(?)
    """
    rows = db.execute_query(query, (sector, sector))
    if not rows:
        raise HTTPException(
            status_code=404, detail=f"Sector '{sector}' not found or has no companies"
        )
    return [dict(r) for r in rows]
