"""
Health check router for FastAPI REST service.
"""

import time
from typing import Dict
from fastapi import APIRouter
from src.database import DatabaseManager

router = APIRouter(tags=["Health"])
START_TIME = time.time()


@router.get("/health")
def get_health() -> Dict:
    """Return API health status, DB row counts for 10 tables, uptime, and version."""
    db = DatabaseManager()
    tables = [
        "companies",
        "sectors",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "stock_prices",
        "financial_ratios",
        "corporate_actions",
        "analysis",
        "documents",
    ]

    counts = {}
    for table in tables:
        try:
            res = db.execute_query(f"SELECT COUNT(*) AS cnt FROM {table}")
            counts[table] = res[0]["cnt"] if res else 0
        except Exception:
            counts[table] = 0

    uptime = round(time.time() - START_TIME, 2)
    return {
        "status": "ok",
        "db_row_counts": counts,
        "uptime_seconds": uptime,
        "version": "1.0.0",
    }
