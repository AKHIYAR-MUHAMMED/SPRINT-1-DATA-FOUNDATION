"""
API Unit tests for /api/v1/screener endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_screener_valid_filter_roe():
    response = client.get("/api/v1/screener?min_roe=15")
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    for comp in results:
        assert comp["return_on_equity_pct"] >= 15.0


def test_screener_invalid_parameter_400():
    response = client.get("/api/v1/screener?max_de=-10")
    assert response.status_code == 400


def test_screener_multiple_filters():
    response = client.get("/api/v1/screener?min_roe=10&max_de=1.5&max_pe=30")
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    for comp in results:
        assert comp["return_on_equity_pct"] >= 10.0
        assert comp["debt_to_equity"] <= 1.5
        assert comp["pe_ratio"] <= 30.0
