"""
Clustering and Profiling Module for N100 Financial Intelligence Platform.
Implements KMeans clustering (5 clusters), elbow curve generation, cluster profiling,
correlation matrix heatmap, outlier detection (Z-score > 3), and portfolio statistics.
"""

import os
import sqlite3
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

DEFAULT_DB_PATH = Path(os.getenv("DB_PATH", "data/db/nifty100.db"))

CLUSTER_NAMES = {
    0: "High-Quality Compounders",
    1: "Defensive Dividend Payers",
    2: "Value Cyclicals",
    3: "Distressed or Turnaround",
    4: "Emerging Growth",
}


def get_latest_company_metrics(db_path: Path = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Fetch latest year financial metrics for all 92 companies from SQLite database."""
    conn = sqlite3.connect(db_path)
    query = """
    SELECT 
        c.ticker AS company_id,
        c.name AS company_name,
        c.sector_name AS broad_sector,
        c.industry AS sub_sector,
        COALESCE(r.return_on_equity_pct, r.roe) AS return_on_equity_pct,
        r.debt_to_equity,
        r.revenue_cagr_5yr,
        r.operating_profit_margin_pct,
        r.free_cash_flow_cr,
        r.return_on_capital_employed_pct AS roce_pct,
        r.pe_ratio,
        r.pb_ratio,
        r.net_profit_margin_pct,
        r.interest_coverage,
        r.cfo_quality_score,
        r.dividend_payout_ratio_pct
    FROM companies c
    LEFT JOIN financial_ratios r ON c.ticker = r.ticker
    AND r.year = (SELECT MAX(year) FROM financial_ratios WHERE ticker = c.ticker)
    """
    df = pd.read_sql_query(query, conn)

    # Calculate 5-yr FCF CAGR where possible or compute ratio from cashflow
    fcf_query = """
    SELECT ticker, year, free_cash_flow_cr 
    FROM financial_ratios 
    ORDER BY ticker, year
    """
    fcf_df = pd.read_sql_query(fcf_query, conn)
    conn.close()

    # Calculate 5-year FCF CAGR for each company
    fcf_cagrs = {}
    for ticker, group in fcf_df.groupby("ticker"):
        group = group.dropna(subset=["free_cash_flow_cr"])
        if len(group) >= 5:
            start_val = group.iloc[-5]["free_cash_flow_cr"]
            end_val = group.iloc[-1]["free_cash_flow_cr"]
            if start_val > 0 and end_val > 0:
                cagr = (end_val / start_val) ** (1.0 / 5.0) - 1.0
                fcf_cagrs[ticker] = round(cagr * 100, 2)
            else:
                fcf_cagrs[ticker] = np.nan
        else:
            fcf_cagrs[ticker] = np.nan

    df["fcf_cagr_5yr"] = df["company_id"].map(fcf_cagrs)
    return df


def run_kmeans_clustering(
    db_path: Path = DEFAULT_DB_PATH,
    output_dir: Path = Path("output"),
    reports_dir: Path = Path("reports"),
) -> pd.DataFrame:
    """Perform KMeans clustering (k=5) on 92 companies after sector median imputation

    and StandardScaler normalization. Generates elbow plot and cluster_labels.csv.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    df = get_latest_company_metrics(db_path)

    features = [
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "fcf_cagr_5yr",
        "operating_profit_margin_pct",
    ]

    # Impute missing values with sector median for each metric
    for col in features:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        sector_medians = df.groupby("broad_sector")[col].transform("median")
        df[col] = df[col].fillna(sector_medians)
        # Global median fallback if sector median is NaN
        df[col] = df[col].fillna(df[col].median()).fillna(0.0)

    # Standard scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features])

    # Elbow curve (inertia for k in 2..10)
    inertias = []
    k_range = list(range(2, 11))
    for k in k_range:
        km_test = KMeans(n_clusters=k, random_state=42, n_init=10)
        km_test.fit(X_scaled)
        inertias.append(km_test.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(k_range, inertias, marker="o", linestyle="--", color="#1f77b4")
    plt.axvline(x=5, color="red", linestyle=":", label="Selected k=5")
    plt.title("KMeans Elbow Plot (Inertia vs k)")
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Inertia")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    elbow_path = reports_dir / "elbow_plot.png"
    plt.savefig(elbow_path, dpi=300)
    plt.close()

    # Fit final KMeans with k=5, random_state=42
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    df["cluster_id"] = cluster_labels
    df["cluster_name"] = df["cluster_id"].map(CLUSTER_NAMES)

    # Compute distance from centroid
    centroids = kmeans.cluster_centers_
    distances = []
    for idx, row in enumerate(X_scaled):
        c_id = cluster_labels[idx]
        dist = np.linalg.norm(row - centroids[c_id])
        distances.append(round(dist, 4))
    df["distance_from_centroid"] = distances

    # Export output/cluster_labels.csv
    export_df = df[
        ["company_id", "cluster_id", "cluster_name", "distance_from_centroid"]
    ]
    export_df.to_csv(output_dir / "cluster_labels.csv", index=False)

    return df


def generate_cluster_reports_and_stats(
    db_path: Path = DEFAULT_DB_PATH,
    output_dir: Path = Path("output"),
    reports_dir: Path = Path("reports"),
) -> None:
    """Generate correlation heatmap, outlier Z-score report, and portfolio stats."""
    output_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    df = run_kmeans_clustering(db_path, output_dir, reports_dir)

    # Correlation Matrix Heatmap of 10 KPIs
    kpi_cols = [
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "fcf_cagr_5yr",
        "operating_profit_margin_pct",
        "roce_pct",
        "pe_ratio",
        "pb_ratio",
        "net_profit_margin_pct",
        "interest_coverage",
    ]

    for col in kpi_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median()).fillna(0.0)

    plt.figure(figsize=(10, 8))
    corr_matrix = df[kpi_cols].corr()
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        square=True,
        linewidths=0.5,
    )
    plt.title("10 KPI Pearson Correlation Matrix Heatmap (N=92 Companies)")
    plt.tight_layout()
    plt.savefig(reports_dir / "correlation_heatmap.png", dpi=300)
    plt.close()

    # Outlier Detection: Z-score > 3 per broad_sector
    outliers = []
    for sector, group in df.groupby("broad_sector"):
        for col in kpi_cols:
            vals = group[col]
            if len(vals) > 1 and vals.std() > 0:
                z_scores = stats.zscore(vals)
                for i, z in enumerate(z_scores):
                    if abs(z) > 3.0:
                        outliers.append(
                            {
                                "company_id": group.iloc[i]["company_id"],
                                "company_name": group.iloc[i]["company_name"],
                                "broad_sector": sector,
                                "metric": col,
                                "value": group.iloc[i][col],
                                "z_score": round(z, 2),
                            }
                        )

    outlier_df = (
        pd.DataFrame(outliers)
        if outliers
        else pd.DataFrame(
            columns=[
                "company_id",
                "company_name",
                "broad_sector",
                "metric",
                "value",
                "z_score",
            ]
        )
    )
    outlier_df.to_csv(output_dir / "outlier_report.csv", index=False)

    # Portfolio Stats: P10, P25, P50, P75, P90, Mean, Std
    stats_data = []
    for col in kpi_cols:
        series = df[col]
        stats_data.append(
            {
                "kpi": col,
                "P10": round(series.quantile(0.10), 2),
                "P25": round(series.quantile(0.25), 2),
                "P50": round(series.quantile(0.50), 2),
                "P75": round(series.quantile(0.75), 2),
                "P90": round(series.quantile(0.90), 2),
                "Mean": round(series.mean(), 2),
                "Std": round(series.std(), 2),
            }
        )

    portfolio_stats_df = pd.DataFrame(stats_data)
    portfolio_stats_df.to_csv(output_dir / "portfolio_stats.csv", index=False)


if __name__ == "__main__":
    generate_cluster_reports_and_stats()
