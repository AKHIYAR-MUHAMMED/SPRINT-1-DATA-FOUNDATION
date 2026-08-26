"""
API Unit tests for /api/v1/sectors endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_list_sectors():
    response = client.get("/api/v1/sectors")
    assert response.status_code == 200
    sectors = response.json()
    assert isinstance(sectors, list)
    assert len(sectors) >= 5


def test_get_sector_companies_valid():
    response = client.get("/api/v1/sectors/Technology/companies")
    assert response.status_code == 200
    companies = response.json()
    assert isinstance(companies, list)
    for comp in companies:
        assert comp["sector_name"].lower() == "technology" or comp["sub_sector"].lower() == "technology"


def test_get_sector_companies_invalid_404():
    response = client.get("/api/v1/sectors/INVALID_SECTOR_NAME_999/companies")
    assert response.status_code == 404
