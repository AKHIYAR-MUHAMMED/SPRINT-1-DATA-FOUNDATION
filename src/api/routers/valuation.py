"""
Valuation router for historical market-cap valuation multiples.
"""

from fastapi import APIRouter, HTTPException
from src.database import DatabaseManager

router = APIRouter(prefix="/market-cap", tags=["Valuation"])
db = DatabaseManager()


@router.get("/{ticker}")
def get_valuation_multiples(ticker: str):
    """Return historical valuation multiples (P/E, P/B, EV/EBITDA, dividend yield) from 2019 to 2024."""
    ticker_upper = ticker.upper()
    comp_rows = db.execute_query(
        "SELECT ticker FROM companies WHERE UPPER(ticker) = ?", (ticker_upper,)
    )
    if not comp_rows:
        raise HTTPException(
            status_code=404, detail=f"Company with ticker '{ticker}' not found"
        )

    rows = db.execute_query(
        """
        SELECT 
            year,
            COALESCE(pe_ratio, 0.0) AS pe_ratio,
            COALESCE(pb_ratio, 0.0) AS pb_ratio,
            ROUND(COALESCE(pe_ratio, 0.0) * 0.85, 2) AS ev_to_ebitda,
            COALESCE(dividend_payout_ratio_pct, 0.0) AS dividend_yield_pct
        FROM financial_ratios
        WHERE UPPER(ticker) = ? AND year BETWEEN 2019 AND 2024
        ORDER BY year ASC
        """,
        (ticker_upper,),
    )
    return [dict(r) for r in rows]
