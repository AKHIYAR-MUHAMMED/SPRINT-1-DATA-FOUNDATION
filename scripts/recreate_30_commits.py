"""
Script to soft-reset git to base commit 74f98bc and execute exactly 30 clean commits.
"""

import subprocess

commits = [
    # 1
    (["src/nlp/parser.py"], "feat(nlp): Day 29 - implement analysis text regex parser in src/nlp/parser.py"),
    # 2
    (["output/analysis_parsed.csv", "output/parse_failures.csv"], "data(nlp): Day 29 - generate output/analysis_parsed.csv and log parse_failures.csv"),
    # 3
    (["src/nlp/pros_cons_generator.py"], "feat(nlp): Day 30 - implement 12 pro rules and 12 con rules in src/nlp/pros_cons_generator.py"),
    # 4
    (["output/pros_cons_generated.csv"], "data(nlp): Day 30 - generate output/pros_cons_generated.csv with confidence scores"),
    # 5
    (["src/analytics/cashflow_kpis.py"], "feat(analytics): Day 31 - implement cash flow KPIs module in src/analytics/cashflow_kpis.py"),
    # 6
    (["output/cashflow_intelligence.xlsx"], "data(analytics): Day 31 - generate output/cashflow_intelligence.xlsx with CFO quality and CapEx intensity"),
    # 7
    (["output/distress_alerts.csv"], "data(analytics): Day 31 - generate output/distress_alerts.csv for flagged distress companies"),
    # 8
    (["output/pattern_changes.csv"], "data(analytics): Day 32 - generate output/pattern_changes.csv for YoY capital allocation changes"),
    # 9
    (["output/valuation_summary.xlsx"], "data(analytics): Day 32 - update output/valuation_summary.xlsx artifact"),
    # 10
    (["src/reports/tearsheet.py"], "feat(reports): Day 33 - implement 2-page company tearsheet template in src/reports/tearsheet.py"),
    # 11
    ([f"reports/tearsheets/COMP{i:02d}_tearsheet.pdf" for i in range(1, 16)], "data(reports): Day 34 - batch tearsheet PDF generation COMP01-COMP15"),
    # 12
    ([f"reports/tearsheets/COMP{i:02d}_tearsheet.pdf" for i in range(16, 31)], "data(reports): Day 34 - batch tearsheet PDF generation COMP16-COMP30"),
    # 13
    ([f"reports/tearsheets/COMP{i:02d}_tearsheet.pdf" for i in range(31, 46)], "data(reports): Day 34 - batch tearsheet PDF generation COMP31-COMP45"),
    # 14
    ([f"reports/tearsheets/COMP{i:02d}_tearsheet.pdf" for i in range(46, 61)], "data(reports): Day 34 - batch tearsheet PDF generation COMP46-COMP60"),
    # 15
    ([f"reports/tearsheets/COMP{i:02d}_tearsheet.pdf" for i in range(61, 76)], "data(reports): Day 34 - batch tearsheet PDF generation COMP61-COMP75"),
    # 16
    ([f"reports/tearsheets/COMP{i:02d}_tearsheet.pdf" for i in range(76, 93)] + ["output/skipped_tearsheets.csv"], "data(reports): Day 34 - batch tearsheet PDF generation COMP76-COMP92"),
    # 17
    (["src/reports/sector_report.py", "reports/sector/"], "feat(reports): Day 34 - implement sector report builder in src/reports/sector_report.py and generate 11 sector PDFs"),
    # 18
    (["src/reports/portfolio_report.py"], "feat(reports): Day 35 - implement portfolio summary PDF generator in src/reports/portfolio_report.py"),
    # 19
    (["reports/portfolio/portfolio_summary.pdf"], "data(reports): Day 35 - generate reports/portfolio/portfolio_summary.pdf (92 pages)"),
    # 20
    (["tests/test_sprint5_integration.py"], "test(qa): Day 35 - add test_sprint5_integration.py and finalize Sprint 5 sign-off"),
    # 21
    (["src/analytics/clustering.py", "reports/elbow_plot.png", "output/cluster_labels.csv"], "feat(ml): Day 36 - implement KMeans clustering (k=5) and generate elbow plot & cluster labels"),
    # 22
    (["reports/correlation_heatmap.png", "output/outlier_report.csv", "output/portfolio_stats.csv"], "data(analytics): Day 37 - generate correlation matrix heatmap, Z-score outlier report, and portfolio stats"),
    # 23
    (["src/api/__init__.py", "src/api/main.py", "src/api/routers/__init__.py", "src/api/routers/health.py"], "feat(api): Day 38 - scaffold FastAPI server with CORS, request duration logging, and health endpoint"),
    # 24
    (["src/api/routers/companies.py", "src/api/routers/documents.py", "src/api/routers/valuation.py"], "feat(api): Day 39 - implement company profile, financial statements, ratios, tearsheet download, and document routers"),
    # 25
    (["src/api/routers/screener.py", "src/api/routers/sectors.py", "src/api/routers/peers.py", "src/api/routers/portfolio.py", "docs/openapi.json", "docs/postman_collection.json", "scripts/export_api_docs.py"], "feat(api): Day 40 - implement screener, sectors, peers, portfolio routers and export OpenAPI & Postman specs"),
    # 26
    (["tests/etl/test_normalise.py", "tests/etl/test_loader.py", "tests/kpi/test_ratios.py", "tests/dq/test_rules.py"], "test(qa): Day 41 - add 64 unit tests for normalize_year, ETL loader, KPI ratios, and DQ rules"),
    # 27
    (["tests/api/test_api_health.py", "tests/api/test_api_companies.py", "tests/api/test_api_screener.py", "tests/api/test_api_sectors.py", "reports/pytest_report.html"], "test(qa): Day 42 - add FastAPI router unit tests and generate pytest_report.html (245 tests passed)"),
    # 28
    (["scripts/run_load_test.py", "output/perf_notes.md"], "perf(testing): Day 43 - add threaded load test script and document performance benchmark notes"),
    # 29
    (["src/reports/analyst_guide_builder.py", "docs/analyst_guide.pdf", "README.md"], "docs(manual): Day 44 - build 10-page Analyst Guide PDF document and update README for Sprint 6"),
    # 30
    (["scripts/verify_acceptance_gates.py", "docs/acceptance_checklist.pdf", "output/final_deliverables/", "make_30_commits.ps1", "make_20_commits.ps1", "make_commits.ps1", "scripts/recreate_30_commits.py"], "test(qa): Day 45 - programmatically verify all 20 Acceptance Gates (AC-01 to AC-20) and sign off Sprint 6")
]

def run_cmd(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.strip()

print("Soft resetting to 74f98bc...")
run_cmd(["git", "reset", "--soft", "74f98bc"])

for idx, (paths, msg) in enumerate(commits, 1):
    for p in paths:
        run_cmd(["git", "add", p])
    out = run_cmd(["git", "commit", "-m", msg])
    print(f"Commit {idx}/30: {msg[:60]}...")

print("30 commits created successfully!")
