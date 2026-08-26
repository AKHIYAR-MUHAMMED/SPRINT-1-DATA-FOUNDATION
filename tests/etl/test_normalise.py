"""
20 Unit tests for normalize_year() in src/etl/normaliser.py
"""

import datetime
import pytest
import numpy as np
import pandas as pd
from src.etl.normaliser import normalize_year


def test_normalise_year_int():
    assert normalize_year(2024) == 2024


def test_normalise_year_float():
    assert normalize_year(2024.0) == 2024


def test_normalise_year_string_4digit():
    assert normalize_year("2024") == 2024


def test_normalise_year_string_float():
    assert normalize_year("2024.0") == 2024


def test_normalise_year_2digit_under_50():
    assert normalize_year(24) == 2024


def test_normalise_year_2digit_over_50():
    assert normalize_year(99) == 1999


def test_normalise_year_2digit_string_under_50():
    assert normalize_year("24") == 2024


def test_normalise_year_2digit_string_over_50():
    assert normalize_year("85") == 1985


def test_normalise_year_excel_single_quote():
    assert normalize_year("'2024") == 2024


def test_normalise_year_datetime_date():
    assert normalize_year(datetime.date(2025, 5, 12)) == 2025


def test_normalise_year_datetime_datetime():
    assert normalize_year(datetime.datetime(2023, 10, 1, 12, 30)) == 2023


def test_normalise_year_pandas_timestamp():
    assert normalize_year(pd.Timestamp("2022-04-15")) == 2022


def test_normalise_year_date_string():
    assert normalize_year("2021-03-31") == 2021


def test_normalise_year_np_integer():
    assert normalize_year(np.int64(2020)) == 2020


def test_normalise_year_none_raises():
    with pytest.raises(ValueError):
        normalize_year(None)


def test_normalise_year_nan_raises():
    with pytest.raises(ValueError):
        normalize_year(np.nan)


def test_normalise_year_bool_raises():
    with pytest.raises(TypeError):
        normalize_year(True)


def test_normalise_year_empty_str_raises():
    with pytest.raises(ValueError):
        normalize_year("   ")


def test_normalise_year_out_of_bounds_raises():
    with pytest.raises(ValueError):
        normalize_year(10050)


def test_normalise_year_invalid_str_raises():
    with pytest.raises(ValueError):
        normalize_year("invalid_year_str")
