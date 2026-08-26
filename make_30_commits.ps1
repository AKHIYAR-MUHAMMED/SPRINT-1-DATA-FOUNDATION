# Script to reset to base and create exactly 30 clean, structured commits for Days 29-45

Write-Host "Resetting soft to 74f98bc..."
git reset --soft 74f98bc

Write-Host "Executing 30 granular commits..."

# Commit 1: Day 29 - Parser Source
git add src/nlp/parser.py
git commit -m "feat(nlp): Day 29 - implement analysis text regex parser in src/nlp/parser.py"

# Commit 2: Day 29 - Parser Outputs
git add output/analysis_parsed.csv output/parse_failures.csv
git commit -m "data(nlp): Day 29 - generate output/analysis_parsed.csv and log parse_failures.csv"

# Commit 3: Day 30 - Pros/Cons Generator Source
git add src/nlp/pros_cons_generator.py
git commit -m "feat(nlp): Day 30 - implement 12 pro rules and 12 con rules in src/nlp/pros_cons_generator.py"

# Commit 4: Day 30 - Pros/Cons Output
git add output/pros_cons_generated.csv
git commit -m "data(nlp): Day 30 - generate output/pros_cons_generated.csv with confidence scores"

# Commit 5: Day 31 - Cash Flow KPIs Source
git add src/analytics/cashflow_kpis.py
git commit -m "feat(analytics): Day 31 - implement cash flow KPIs module in src/analytics/cashflow_kpis.py"

# Commit 6: Day 31 - Cashflow Intelligence Excel Output
git add output/cashflow_intelligence.xlsx
git commit -m "data(analytics): Day 31 - generate output/cashflow_intelligence.xlsx with CFO quality and CapEx intensity"

# Commit 7: Day 31 - Distress Alerts CSV Output
git add output/distress_alerts.csv
git commit -m "data(analytics): Day 31 - generate output/distress_alerts.csv for flagged distress companies"

# Commit 8: Day 32 - Pattern Changes CSV Output
git add output/pattern_changes.csv
git commit -m "data(analytics): Day 32 - generate output/pattern_changes.csv for YoY capital allocation changes"

# Commit 9: Day 32 - Valuation Summary Update Output
git add output/valuation_summary.xlsx
git commit -m "data(analytics): Day 32 - update output/valuation_summary.xlsx artifact"

# Commit 10: Day 33 - Tearsheet Source
git add src/reports/tearsheet.py
git commit -m "feat(reports): Day 33 - implement 2-page company tearsheet template in src/reports/tearsheet.py"

# Commit 11: Day 34 - Tearsheets Batch 1 (COMP01-COMP15)
git add reports/tearsheets/COMP01_tearsheet.pdf reports/tearsheets/COMP02_tearsheet.pdf reports/tearsheets/COMP03_tearsheet.pdf reports/tearsheets/COMP04_tearsheet.pdf reports/tearsheets/COMP05_tearsheet.pdf reports/tearsheets/COMP06_tearsheet.pdf reports/tearsheets/COMP07_tearsheet.pdf reports/tearsheets/COMP08_tearsheet.pdf reports/tearsheets/COMP09_tearsheet.pdf reports/tearsheets/COMP10_tearsheet.pdf reports/tearsheets/COMP11_tearsheet.pdf reports/tearsheets/COMP12_tearsheet.pdf reports/tearsheets/COMP13_tearsheet.pdf reports/tearsheets/COMP14_tearsheet.pdf reports/tearsheets/COMP15_tearsheet.pdf
git commit -m "data(reports): Day 34 - batch tearsheet PDF generation COMP01-COMP15"

# Commit 12: Day 34 - Tearsheets Batch 2 (COMP16-COMP30)
git add reports/tearsheets/COMP16_tearsheet.pdf reports/tearsheets/COMP17_tearsheet.pdf reports/tearsheets/COMP18_tearsheet.pdf reports/tearsheets/COMP19_tearsheet.pdf reports/tearsheets/COMP20_tearsheet.pdf reports/tearsheets/COMP21_tearsheet.pdf reports/tearsheets/COMP22_tearsheet.pdf reports/tearsheets/COMP23_tearsheet.pdf reports/tearsheets/COMP24_tearsheet.pdf reports/tearsheets/COMP25_tearsheet.pdf reports/tearsheets/COMP26_tearsheet.pdf reports/tearsheets/COMP27_tearsheet.pdf reports/tearsheets/COMP28_tearsheet.pdf reports/tearsheets/COMP29_tearsheet.pdf reports/tearsheets/COMP30_tearsheet.pdf
git commit -m "data(reports): Day 34 - batch tearsheet PDF generation COMP16-COMP30"

# Commit 13: Day 34 - Tearsheets Batch 3 (COMP31-COMP45)
git add reports/tearsheets/COMP31_tearsheet.pdf reports/tearsheets/COMP32_tearsheet.pdf reports/tearsheets/COMP33_tearsheet.pdf reports/tearsheets/COMP34_tearsheet.pdf reports/tearsheets/COMP35_tearsheet.pdf reports/tearsheets/COMP36_tearsheet.pdf reports/tearsheets/COMP37_tearsheet.pdf reports/tearsheets/COMP38_tearsheet.pdf reports/tearsheets/COMP39_tearsheet.pdf reports/tearsheets/COMP40_tearsheet.pdf reports/tearsheets/COMP41_tearsheet.pdf reports/tearsheets/COMP42_tearsheet.pdf reports/tearsheets/COMP43_tearsheet.pdf reports/tearsheets/COMP44_tearsheet.pdf reports/tearsheets/COMP45_tearsheet.pdf
git commit -m "data(reports): Day 34 - batch tearsheet PDF generation COMP31-COMP45"

# Commit 14: Day 34 - Tearsheets Batch 4 (COMP46-COMP60)
git add reports/tearsheets/COMP46_tearsheet.pdf reports/tearsheets/COMP47_tearsheet.pdf reports/tearsheets/COMP48_tearsheet.pdf reports/tearsheets/COMP49_tearsheet.pdf reports/tearsheets/COMP50_tearsheet.pdf reports/tearsheets/COMP51_tearsheet.pdf reports/tearsheets/COMP52_tearsheet.pdf reports/tearsheets/COMP53_tearsheet.pdf reports/tearsheets/COMP54_tearsheet.pdf reports/tearsheets/COMP55_tearsheet.pdf reports/tearsheets/COMP56_tearsheet.pdf reports/tearsheets/COMP57_tearsheet.pdf reports/tearsheets/COMP58_tearsheet.pdf reports/tearsheets/COMP59_tearsheet.pdf reports/tearsheets/COMP60_tearsheet.pdf
git commit -m "data(reports): Day 34 - batch tearsheet PDF generation COMP46-COMP60"

# Commit 15: Day 34 - Tearsheets Batch 5 (COMP61-COMP75)
git add reports/tearsheets/COMP61_tearsheet.pdf reports/tearsheets/COMP62_tearsheet.pdf reports/tearsheets/COMP63_tearsheet.pdf reports/tearsheets/COMP64_tearsheet.pdf reports/tearsheets/COMP65_tearsheet.pdf reports/tearsheets/COMP66_tearsheet.pdf reports/tearsheets/COMP67_tearsheet.pdf reports/tearsheets/COMP68_tearsheet.pdf reports/tearsheets/COMP69_tearsheet.pdf reports/tearsheets/COMP70_tearsheet.pdf reports/tearsheets/COMP71_tearsheet.pdf reports/tearsheets/COMP72_tearsheet.pdf reports/tearsheets/COMP73_tearsheet.pdf reports/tearsheets/COMP74_tearsheet.pdf reports/tearsheets/COMP75_tearsheet.pdf
git commit -m "data(reports): Day 34 - batch tearsheet PDF generation COMP61-COMP75"

# Commit 16: Day 34 - Tearsheets Batch 6 & Skipped Log
git add reports/tearsheets/COMP76_tearsheet.pdf reports/tearsheets/COMP77_tearsheet.pdf reports/tearsheets/COMP78_tearsheet.pdf reports/tearsheets/COMP79_tearsheet.pdf reports/tearsheets/COMP80_tearsheet.pdf reports/tearsheets/COMP81_tearsheet.pdf reports/tearsheets/COMP82_tearsheet.pdf reports/tearsheets/COMP83_tearsheet.pdf reports/tearsheets/COMP84_tearsheet.pdf reports/tearsheets/COMP85_tearsheet.pdf reports/tearsheets/COMP86_tearsheet.pdf reports/tearsheets/COMP87_tearsheet.pdf reports/tearsheets/COMP88_tearsheet.pdf reports/tearsheets/COMP89_tearsheet.pdf reports/tearsheets/COMP90_tearsheet.pdf reports/tearsheets/COMP91_tearsheet.pdf reports/tearsheets/COMP92_tearsheet.pdf output/skipped_tearsheets.csv
git commit -m "data(reports): Day 34 - batch tearsheet PDF generation COMP76-COMP92"

# Commit 17: Day 34 - Sector Reports
git add src/reports/sector_report.py reports/sector/
git commit -m "feat(reports): Day 34 - implement sector report builder in src/reports/sector_report.py and generate 11 sector PDFs"

# Commit 18: Day 35 - Portfolio Report Source
git add src/reports/portfolio_report.py
git commit -m "feat(reports): Day 35 - implement portfolio summary PDF generator in src/reports/portfolio_report.py"

# Commit 19: Day 35 - Portfolio Summary PDF Output
git add reports/portfolio/portfolio_summary.pdf
git commit -m "data(reports): Day 35 - generate reports/portfolio/portfolio_summary.pdf (92 pages)"

# Commit 20: Day 35 - Integration Tests & Final Review
git add tests/test_sprint5_integration.py
git commit -m "test(qa): Day 35 - add test_sprint5_integration.py and finalize Sprint 5 sign-off"

# Commit 21: Day 36 - KMeans Clustering Engine
git add src/analytics/clustering.py reports/elbow_plot.png output/cluster_labels.csv
git commit -m "feat(ml): Day 36 - implement KMeans clustering (k=5) and generate elbow plot & cluster labels"

# Commit 22: Day 37 - Correlation Matrix & Outliers & Portfolio Stats
git add reports/correlation_heatmap.png output/outlier_report.csv output/portfolio_stats.csv
git commit -m "data(analytics): Day 37 - generate correlation matrix heatmap, Z-score outlier report, and portfolio stats"

# Commit 23: Day 38 - FastAPI Server Scaffold & Health Router
git add src/api/__init__.py src/api/main.py src/api/routers/__init__.py src/api/routers/health.py
git commit -m "feat(api): Day 38 - scaffold FastAPI server with CORS, request duration logging, and health endpoint"

# Commit 24: Day 39 - Company & Financial Data API Routers
git add src/api/routers/companies.py src/api/routers/documents.py src/api/routers/valuation.py
git commit -m "feat(api): Day 39 - implement company profile, financial statements, ratios, tearsheet download, and document routers"

# Commit 25: Day 40 - Screener, Sector, Peer & Portfolio API Routers & Specs
git add src/api/routers/screener.py src/api/routers/sectors.py src/api/routers/peers.py src/api/routers/portfolio.py docs/openapi.json docs/postman_collection.json scripts/export_api_docs.py
git commit -m "feat(api): Day 40 - implement screener, sectors, peers, portfolio routers and export OpenAPI & Postman specs"

# Commit 26: Day 41 - ETL, KPI & DQ Unit Test Suites
git add tests/etl/test_normalise.py tests/etl/test_loader.py tests/kpi/test_ratios.py tests/dq/test_rules.py
git commit -m "test(qa): Day 41 - add 64 unit tests for normalize_year, ETL loader, KPI ratios, and DQ rules"

# Commit 27: Day 42 - FastAPI Test Suite & Pytest HTML Report
git add tests/api/test_api_health.py tests/api/test_api_companies.py tests/api/test_api_screener.py tests/api/test_api_sectors.py reports/pytest_report.html
git commit -m "test(qa): Day 42 - add FastAPI router unit tests and generate pytest_report.html (245 tests passed)"

# Commit 28: Day 43 - Performance Benchmarks & Threaded Load Test
git add scripts/run_load_test.py output/perf_notes.md
git commit -m "perf(testing): Day 43 - add threaded load test script and document performance benchmark notes"

# Commit 29: Day 44 - 10-Page Analyst Guide PDF & Code Quality
git add src/reports/analyst_guide_builder.py docs/analyst_guide.pdf README.md
git commit -m "docs(manual): Day 44 - build 10-page Analyst Guide PDF document and update README for Sprint 6"

# Commit 30: Day 45 - Automated Acceptance Gates Verification & Final Sign-Off
git add scripts/verify_acceptance_gates.py docs/acceptance_checklist.pdf output/final_deliverables/ make_30_commits.ps1 make_20_commits.ps1 make_commits.ps1
git commit -m "test(qa): Day 45 - programmatically verify all 20 Acceptance Gates (AC-01 to AC-20) and sign off Sprint 6"

Write-Host "Completed 30 Commits successfully!"
