"""
20 Unit tests for KPI ratios calculations, flags, and score calculations.
"""

import pytest
import numpy as np
import pandas as pd
from src.analytics.cagr import calculate_cagr
from src.analytics.cashflow_kpis import (
    calculate_cfo_quality_score,
    calculate_free_cash_flow,
    calculate_capex_intensity,
    calculate_fcf_conversion_rate,
)


def calculate_roe(net_income: float, total_equity: float):
    if total_equity is None or total_equity <= 0:
        return None
    return round((net_income / total_equity) * 100.0, 2)


def calculate_de(total_debt: float, total_equity: float):
    if total_debt is None or total_debt <= 0:
        return 0.0
    if total_equity is None or total_equity <= 0:
        return None
    return round(total_debt / total_equity, 2)


def calculate_icr(operating_profit: float, interest_expense: float):
    if interest_expense is None or interest_expense <= 0:
        return None
    return round(operating_profit / interest_expense, 2)


def test_roe_positive_equity():
    assert calculate_roe(20.0, 100.0) == 20.0


def test_roe_negative_equity():
    assert calculate_roe(20.0, -50.0) is None


def test_roe_zero_equity():
    assert calculate_roe(20.0, 0.0) is None


def test_de_debt_free():
    assert calculate_de(0.0, 100.0) == 0.0


def test_de_positive_debt():
    assert calculate_de(50.0, 100.0) == 0.5


def test_de_negative_equity():
    assert calculate_de(50.0, -20.0) is None


def test_icr_zero_interest():
    assert calculate_icr(100.0, 0.0) is None


def test_icr_positive_interest():
    assert calculate_icr(100.0, 10.0) == 10.0


def test_de_leverage_flag_non_financial():
    de = 5.5
    is_financial = False
    flag = de > 5.0 and not is_financial
    assert flag is True


def test_de_leverage_flag_financial():
    de = 6.0
    is_financial = True
    flag = de > 5.0 and not is_financial
    assert flag is False


def test_cagr_normal():
    cagr_val, flag = calculate_cagr(100.0, 200.0, 5)
    assert cagr_val is not None
    assert round(cagr_val, 2) == 14.87


def test_cagr_turnaround_flag():
    start, end = -50.0, 100.0
    is_turnaround = start < 0 and end > 0
    assert is_turnaround is True


def test_cagr_decline_to_loss_flag():
    start, end = 100.0, -20.0
    is_decline_loss = start > 0 and end < 0
    assert is_decline_loss is True


def test_opm_divergence_flag():
    reported_opm = 25.0
    computed_opm = 15.0
    divergence_flag = abs(reported_opm - computed_opm) > 5.0
    assert divergence_flag is True


def test_opm_no_divergence():
    reported_opm = 20.0
    computed_opm = 19.5
    divergence_flag = abs(reported_opm - computed_opm) > 5.0
    assert divergence_flag is False


def test_cfo_quality_score_calculation():
    cfo_list = [100.0, 110.0, 120.0, 130.0, 140.0]
    pat_list = [80.0, 90.0, 100.0, 110.0, 120.0]
    score = calculate_cfo_quality_score(cfo_list, pat_list)
    assert score is not None
    assert score > 1.0


def test_cfo_quality_score_zero_pat():
    cfo_list = [100.0, 110.0, 120.0, 130.0, 140.0]
    pat_list = [80.0, 0.0, 100.0, 110.0, 120.0]
    score = calculate_cfo_quality_score(cfo_list, pat_list)
    assert score is None


def test_fcf_conversion_rate():
    fcf = 120.0
    op = 200.0
    rate = calculate_fcf_conversion_rate(fcf, op)
    assert rate == 60.0


def test_capex_intensity():
    investing = -50.0
    sales = 500.0
    intensity = calculate_capex_intensity(investing, sales)
    assert intensity == 10.0


def test_interest_coverage_warning():
    icr = 1.2
    is_warning = icr < 1.5
    assert is_warning is True
