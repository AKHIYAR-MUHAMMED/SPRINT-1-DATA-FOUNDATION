"""
10 Unit tests verifying loader reads correct row counts and column schemas.
"""

import pandas as pd
import pytest
from src.database import DatabaseManager
from src.etl.loader import ETLLoader


@pytest.fixture
def db_conn():
    db = DatabaseManager()
    return db


def test_loader_companies_count(db_conn):
    rows = db_conn.execute_query("SELECT COUNT(*) AS cnt FROM companies")
    assert rows[0]["cnt"] == 92


def test_loader_companies_columns(db_conn):
    rows = db_conn.execute_query("SELECT * FROM companies LIMIT 1")
    cols = list(rows[0].keys())
    assert "ticker" in cols
    assert "name" in cols
    assert "sector_name" in cols


def test_loader_sectors_count(db_conn):
    rows = db_conn.execute_query("SELECT COUNT(*) AS cnt FROM sectors")
    assert rows[0]["cnt"] >= 5


def test_loader_pnl_count(db_conn):
    rows = db_conn.execute_query("SELECT COUNT(*) AS cnt FROM profitandloss")
    assert rows[0]["cnt"] >= 1100


def test_loader_pnl_columns(db_conn):
    rows = db_conn.execute_query("SELECT * FROM profitandloss LIMIT 1")
    cols = list(rows[0].keys())
    assert "ticker" in cols
    assert "year" in cols
    assert "sales" in cols
    assert "net_income" in cols


def test_loader_bs_count(db_conn):
    rows = db_conn.execute_query("SELECT COUNT(*) AS cnt FROM balancesheet")
    assert rows[0]["cnt"] >= 1100


def test_loader_cashflow_count(db_conn):
    rows = db_conn.execute_query("SELECT COUNT(*) AS cnt FROM cashflow")
    assert rows[0]["cnt"] >= 1100


def test_loader_financial_ratios_count(db_conn):
    rows = db_conn.execute_query("SELECT COUNT(*) AS cnt FROM financial_ratios")
    assert rows[0]["cnt"] >= 1100


def test_loader_stock_prices_count(db_conn):
    rows = db_conn.execute_query("SELECT COUNT(*) AS cnt FROM stock_prices")
    assert rows[0]["cnt"] >= 5000


def test_loader_documents_count(db_conn):
    rows = db_conn.execute_query("SELECT COUNT(*) AS cnt FROM documents")
    assert rows[0]["cnt"] >= 5
