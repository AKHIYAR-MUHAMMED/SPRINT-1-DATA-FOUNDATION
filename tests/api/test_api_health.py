"""
API Unit tests for /api/v1/health endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health_endpoint_status():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "db_row_counts" in data
    assert "uptime_seconds" in data
    assert data["version"] == "1.0.0"


def test_health_endpoint_table_counts():
    response = client.get("/api/v1/health")
    counts = response.json()["db_row_counts"]
    expected_tables = [
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
    for table in expected_tables:
        assert table in counts
        assert counts[table] >= 0
