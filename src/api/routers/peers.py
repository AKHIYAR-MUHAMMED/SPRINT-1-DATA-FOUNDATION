"""
Peers router for peer group comparisons, percentile ranks, and radar chart metrics.
"""

from fastapi import APIRouter, HTTPException
from src.database import DatabaseManager

router = APIRouter(tags=["Peers"])
db = DatabaseManager()


@router.get("/peers/{group_name}")
def get_peer_group_details(group_name: str):
    """Return all companies in a peer group with percentile ranks across 10 metrics. HTTP 404 if group unknown."""
    rows = db.execute_query(
        """
        SELECT p.ticker AS company_id, c.name AS company_name, p.peer_group, p.metric, p.value, p.percentile_rank, p.year
        FROM peer_percentiles p
        JOIN companies c ON p.ticker = c.ticker
        WHERE UPPER(p.peer_group) = UPPER(?) OR UPPER(c.sector_name) = UPPER(?)
        """,
        (group_name, group_name),
    )
    if not rows:
        # Fallback check on peer_groups table
        pg_rows = db.execute_query(
            "SELECT * FROM peer_groups WHERE UPPER(peer_group_name) = UPPER(?) OR UPPER(sector) = UPPER(?)",
            (group_name, group_name),
        )
        if not pg_rows:
            raise HTTPException(
                status_code=404, detail=f"Peer group '{group_name}' not found"
            )
        return [dict(r) for r in pg_rows]

    return [dict(r) for r in rows]


@router.get("/companies/{ticker}/peers/compare")
def compare_company_peers(ticker: str):
    """Return radar chart metrics (8 axes) for company, peer group average, and benchmark company."""
    ticker_upper = ticker.upper()
    comp_rows = db.execute_query(
        "SELECT ticker, name, sector_name FROM companies WHERE UPPER(ticker) = ?",
        (ticker_upper,),
    )
    if not comp_rows:
        raise HTTPException(
            status_code=404, detail=f"Company '{ticker}' not found"
        )

    company = dict(comp_rows[0])
    sector = company.get("sector_name", "Technology")

    # Fetch latest KPIs for target company
    kpi_rows = db.execute_query(
        "SELECT * FROM financial_ratios WHERE UPPER(ticker) = ? ORDER BY year DESC LIMIT 1",
        (ticker_upper,),
    )
    kpis = dict(kpi_rows[0]) if kpi_rows else {}

    # Define 8 radar axes metrics
    axes = [
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "operating_profit_margin_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "cfo_quality_score",
        "pe_ratio",
    ]

    company_values = {}
    for ax in axes:
        val = kpis.get(ax)
        company_values[ax] = round(float(val), 2) if val is not None else 0.0

    # Sector average values
    sector_avg_query = """
    SELECT 
        AVG(r.return_on_equity_pct) AS return_on_equity_pct,
        AVG(r.return_on_capital_employed_pct) AS return_on_capital_employed_pct,
        AVG(r.operating_profit_margin_pct) AS operating_profit_margin_pct,
        AVG(r.net_profit_margin_pct) AS net_profit_margin_pct,
        AVG(r.debt_to_equity) AS debt_to_equity,
        AVG(r.revenue_cagr_5yr) AS revenue_cagr_5yr,
        AVG(r.cfo_quality_score) AS cfo_quality_score,
        AVG(r.pe_ratio) AS pe_ratio
    FROM companies c
    JOIN financial_ratios r ON c.ticker = r.ticker
    AND r.year = (SELECT MAX(year) FROM financial_ratios WHERE ticker = c.ticker)
    WHERE c.sector_name = ?
    """
    avg_rows = db.execute_query(sector_avg_query, (sector,))
    peer_avg_values = (
        {k: round(float(v), 2) if v else 0.0 for k, v in dict(avg_rows[0]).items()}
        if avg_rows
        else {}
    )

    # Benchmark company (e.g. COMP01 or top company in sector)
    benchmark_query = """
    SELECT ticker FROM companies WHERE sector_name = ? AND ticker != ? LIMIT 1
    """
    bench_rows = db.execute_query(benchmark_query, (sector, ticker_upper))
    bench_ticker = bench_rows[0]["ticker"] if bench_rows else "COMP01"
    bench_kpi_rows = db.execute_query(
        "SELECT * FROM financial_ratios WHERE ticker = ? ORDER BY year DESC LIMIT 1",
        (bench_ticker,),
    )
    bench_kpis = dict(bench_kpi_rows[0]) if bench_kpi_rows else {}
    benchmark_values = {
        ax: round(float(bench_kpis.get(ax)), 2) if bench_kpis.get(ax) else 0.0
        for ax in axes
    }

    return {
        "ticker": ticker_upper,
        "company_name": company["name"],
        "sector": sector,
        "axes": axes,
        "company_metrics": company_values,
        "peer_average": peer_avg_values,
        "benchmark_company": bench_ticker,
        "benchmark_metrics": benchmark_values,
    }
