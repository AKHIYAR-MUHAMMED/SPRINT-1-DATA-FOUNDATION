"""
14 Unit tests for Data Quality Rules (DQ-01 through DQ-16).
Crafts synthetic DataFrames violating each rule and verifies rule_id and severity.
"""

import pandas as pd
from src.etl.validator import SchemaValidator


def test_rule_dq01_duplicate_pk():
    validator = SchemaValidator()
    df = pd.DataFrame({"ticker": ["TCS", "TCS"], "name": ["Tata 1", "Tata 2"]})
    validator.validate_companies(df, "companies.xlsx")
    failures = validator.get_failures_df()
    assert not failures.empty
    assert "DQ-01" in failures["rule_id"].values
    assert "CRITICAL" in failures["severity"].values


def test_rule_dq02_null_pk():
    validator = SchemaValidator()
    df = pd.DataFrame({"ticker": [None, "INFY"], "name": ["Unknown", "Infosys"]})
    validator.validate_companies(df, "companies.xlsx")
    failures = validator.get_failures_df()
    assert not failures.empty
    assert "DQ-02" in failures["rule_id"].values
    assert "CRITICAL" in failures["severity"].values


def test_rule_dq03_referential_integrity():
    validator = SchemaValidator()
    companies_df = pd.DataFrame({"ticker": ["TCS"]})
    pnl_df = pd.DataFrame({"ticker": ["INVALID_TICKER"], "year": [2024]})
    validator.validate_relationships(
        pnl_df, companies_df, "income_statements.xlsx"
    )
    failures = validator.get_failures_df()
    assert not failures.empty
    assert "DQ-03" in failures["rule_id"].values
    assert "CRITICAL" in failures["severity"].values


def test_rule_dq04_bs_balance_mismatch():
    validator = SchemaValidator()
    df = pd.DataFrame(
        {
            "ticker": ["TCS"],
            "year": [2024],
            "total_assets": [1000.0],
            "total_liabilities": [400.0],
            "total_equity": [400.0],  # 1000 != 400 + 400
        }
    )
    validator.validate_financials(df, "balancesheet.xlsx", sheet_type="bs")
    failures = validator.get_failures_df()
    assert not failures.empty
    assert "DQ-04" in failures["rule_id"].values
    assert "WARNING" in failures["severity"].values


def test_rule_dq05_opm_crosscheck_failure():
    validator = SchemaValidator()
    df = pd.DataFrame(
        {
            "ticker": ["TCS"],
            "year": [2024],
            "sales": [1000.0],
            "operating_profit": [200.0],  # Computed OPM = 0.20
            "opm": [0.35],  # Reported OPM = 0.35 (Diff > 0.05)
        }
    )
    validator.validate_financials(df, "income_statements.xlsx", sheet_type="pnl")
    failures = validator.get_failures_df()
    assert not failures.empty
    assert "DQ-05" in failures["rule_id"].values
    assert "WARNING" in failures["severity"].values


def test_rule_dq06_negative_sales():
    validator = SchemaValidator()
    df = pd.DataFrame({"ticker": ["TCS"], "year": [2024], "sales": [-100.0]})
    validator.validate_financials(df, "income_statements.xlsx", sheet_type="pnl")
    failures = validator.get_failures_df()
    assert not failures.empty
    assert "DQ-06" in failures["rule_id"].values
    assert "WARNING" in failures["severity"].values


def test_rule_dq07_cashflow_reconciliation():
    validator = SchemaValidator()
    df = pd.DataFrame(
        {
            "ticker": ["TCS"],
            "year": [2024],
            "beginning_cash": [100.0],
            "net_cash_flow": [50.0],
            "ending_cash": [200.0],  # 200 != 100 + 50
        }
    )
    validator.validate_financials(df, "cashflow.xlsx", sheet_type="cf")
    failures = validator.get_failures_df()
    assert not failures.empty
    assert "DQ-07" in failures["rule_id"].values
    assert "WARNING" in failures["severity"].values


def test_rule_dq08_abnormal_tax_rate():
    validator = SchemaValidator()
    df = pd.DataFrame(
        {
            "ticker": ["TCS"],
            "year": [2024],
            "operating_profit": [100.0],
            "net_income": [150.0],  # Tax rate = (100 - 150)/100 = -0.5 (invalid)
        }
    )
    validator.validate_financials(df, "income_statements.xlsx", sheet_type="pnl")
    failures = validator.get_failures_df()
    assert not failures.empty
    assert "DQ-08" in failures["rule_id"].values
    assert "WARNING" in failures["severity"].values


def test_rule_dq09_negative_stock_price():
    validator = SchemaValidator()
    df = pd.DataFrame(
        {
            "ticker": ["TCS"],
            "date": ["2024-01-01"],
            "open": [-10.0],
            "high": [15.0],
            "low": [5.0],
            "close": [12.0],
        }
    )
    validator.validate_prices(df, "stock_prices.xlsx")
    failures = validator.get_failures_df()
    assert not failures.empty
    assert "DQ-09" in failures["rule_id"].values
    assert "CRITICAL" in failures["severity"].values


def test_rule_dq10_invalid_website_url():
    validator = SchemaValidator()
    df = pd.DataFrame({"ticker": ["TCS"], "website": ["invalid_url_without_domain"]})
    validator.validate_companies(df, "companies.xlsx")
    failures = validator.get_failures_df()
    assert not failures.empty
    assert "DQ-10" in failures["rule_id"].values
    assert "WARNING" in failures["severity"].values


def test_rule_dq11_eps_sign_mismatch():
    validator = SchemaValidator()
    df = pd.DataFrame(
        {"ticker": ["TCS"], "year": [2024], "eps": [-5.0], "net_income": [100.0]}
    )
    validator.validate_financials(df, "income_statements.xlsx", sheet_type="pnl")
    failures = validator.get_failures_df()
    assert not failures.empty
    assert "DQ-11" in failures["rule_id"].values
    assert "WARNING" in failures["severity"].values


def test_rule_dq12_exchange_suffix():
    validator = SchemaValidator()
    df = pd.DataFrame({"ticker": ["TCS.INVALID"]})
    validator.validate_companies(df, "companies.xlsx")
    failures = validator.get_failures_df()
    assert not failures.empty
    assert "DQ-12" in failures["rule_id"].values
    assert "WARNING" in failures["severity"].values


def test_rule_dq14_negative_volume():
    validator = SchemaValidator()
    df = pd.DataFrame(
        {
            "ticker": ["TCS"],
            "date": ["2024-01-01"],
            "open": [100.0],
            "high": [105.0],
            "low": [95.0],
            "close": [102.0],
            "volume": [-500],
        }
    )
    validator.validate_prices(df, "stock_prices.xlsx")
    failures = validator.get_failures_df()
    assert not failures.empty
    assert "DQ-14" in failures["rule_id"].values
    assert "WARNING" in failures["severity"].values


def test_rule_dq15_price_consistency():
    validator = SchemaValidator()
    df = pd.DataFrame(
        {
            "ticker": ["TCS"],
            "date": ["2024-01-01"],
            "open": [100.0],
            "high": [90.0],  # High < Open (Inconsistent!)
            "low": [95.0],
            "close": [102.0],
        }
    )
    validator.validate_prices(df, "stock_prices.xlsx")
    failures = validator.get_failures_df()
    assert not failures.empty
    assert "DQ-15" in failures["rule_id"].values
    assert "WARNING" in failures["severity"].values
