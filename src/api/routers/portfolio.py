"""
Portfolio router for portfolio-wide statistical distribution and percentile tables.
"""

from pathlib import Path
import pandas as pd
from fastapi import APIRouter
from src.database import DatabaseManager

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])
db = DatabaseManager()


@router.get("/stats")
def get_portfolio_stats():
    """Return P10 through P90 percentile table for 10 core KPIs across all 92 companies."""
    stats_file = Path("output/portfolio_stats.csv")
    if stats_file.is_file():
        df = pd.read_csv(stats_file)
        return df.to_dict(orient="records")

    # Fallback dynamic calculation
    query = """
    SELECT 
        COALESCE(r.return_on_equity_pct, r.roe, 0.0) AS return_on_equity_pct,
        COALESCE(r.debt_to_equity, 0.0) AS debt_to_equity,
        COALESCE(r.revenue_cagr_5yr, 0.0) AS revenue_cagr_5yr,
        COALESCE(r.operating_profit_margin_pct, 0.0) AS operating_profit_margin_pct,
        COALESCE(r.return_on_capital_employed_pct, 0.0) AS roce_pct,
        COALESCE(r.pe_ratio, 0.0) AS pe_ratio,
        COALESCE(r.pb_ratio, 0.0) AS pb_ratio,
        COALESCE(r.net_profit_margin_pct, 0.0) AS net_profit_margin_pct,
        COALESCE(r.interest_coverage, 0.0) AS interest_coverage,
        COALESCE(r.cfo_quality_score, 0.0) AS cfo_quality_score
    FROM companies c
    LEFT JOIN financial_ratios r ON c.ticker = r.ticker
    AND r.year = (SELECT MAX(year) FROM financial_ratios WHERE ticker = c.ticker)
    """
    rows = db.execute_query(query)
    df = pd.DataFrame([dict(r) for r in rows])

    stats_list = []
    for col in df.columns:
        series = df[col].astype(float)
        stats_list.append(
            {
                "kpi": col,
                "P10": round(float(series.quantile(0.10)), 2),
                "P25": round(float(series.quantile(0.25)), 2),
                "P50": round(float(series.quantile(0.50)), 2),
                "P75": round(float(series.quantile(0.75)), 2),
                "P90": round(float(series.quantile(0.90)), 2),
                "Mean": round(float(series.mean()), 2),
                "Std": round(float(series.std()), 2),
            }
        )
    return stats_list
