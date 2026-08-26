"""
API Unit tests for /api/v1/companies endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_list_companies_count():
    response = client.get("/api/v1/companies")
    assert response.status_code == 200
    companies = response.json()
    assert len(companies) == 92


def test_get_company_by_ticker_valid():
    response = client.get("/api/v1/companies/COMP01")
    assert response.status_code == 200
    data = response.json()
    assert "company" in data
    assert data["company"]["ticker"] == "COMP01"


def test_get_company_by_ticker_invalid_404():
    response = client.get("/api/v1/companies/NONEXISTENT_TICKER_999")
    assert response.status_code == 404


def test_get_company_pl_history():
    response = client.get("/api/v1/companies/COMP01/pl")
    assert response.status_code == 200
    pl_data = response.json()
    assert isinstance(pl_data, list)
    assert len(pl_data) >= 10


def test_get_company_tearsheet_pdf():
    response = client.get("/api/v1/companies/COMP01/tearsheet")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
