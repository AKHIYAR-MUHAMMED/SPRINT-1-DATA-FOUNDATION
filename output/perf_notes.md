# N100 Platform Performance & Load Benchmark Report

**Date/Time**: 2026-08-26 09:23:05

## 1. Concurrent Screener Load Test (10 Threaded Calls)
- **Total Concurrent Completion Time**: 0.125 seconds (Target: < 10.0s) -> **PASS**
- **Max Response Time**: 0.125 seconds
- **Average Response Time**: 0.112 seconds

## 2. Dashboard Company Profile Latency (5 Tickers)
- **COMP01**: 0.008s (Target: < 3.0s) -> **PASS**
- **COMP02**: 0.010s (Target: < 3.0s) -> **PASS**
- **COMP03**: 0.007s (Target: < 3.0s) -> **PASS**
- **COMP04**: 0.007s (Target: < 3.0s) -> **PASS**
- **COMP05**: 0.007s (Target: < 3.0s) -> **PASS**

## 3. SQLite Database Query Optimization & Indexing
- SQLite WAL Mode (`PRAGMA journal_mode=WAL`) & Memory Cache enabled.
- Compound indexes present on `(ticker, year)` in `financial_ratios`, `profitandloss`, `balancesheet`, `cashflow`.
- Single index present on `ticker` in `companies` and `stock_prices`.
- Zero query bottlenecks detected.
