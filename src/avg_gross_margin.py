import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sample_sales_margin_data.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

LOW_MARGIN_THRESHOLD = 0.20


def load_data(file_path: Path) -> pd.DataFrame:
    """Load sample sales margin data."""
    return pd.read_csv(file_path)


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Identify data quality issues that could affect margin reporting."""
    issues = []

    duplicate_ids = df[df.duplicated(subset=["transaction_id"], keep=False)]

    for idx, row in df.iterrows():
        row_issues = []

        if pd.isna(row["transaction_id"]) or str(row["transaction_id"]).strip() == "":
            row_issues.append("Missing transaction_id")

        if row["transaction_id"] in duplicate_ids["transaction_id"].values:
            row_issues.append("Duplicate transaction_id")

        if pd.isna(row["revenue"]):
            row_issues.append("Missing revenue")
        elif row["revenue"] <= 0:
            row_issues.append("Revenue less than or equal to zero")

        if pd.isna(row["cost_of_goods_sold"]):
            row_issues.append("Missing cost_of_goods_sold")
        elif row["cost_of_goods_sold"] < 0:
            row_issues.append("Cost of goods sold less than zero")

        if row_issues:
            issues.append(
                {
                    "transaction_id": row["transaction_id"],
                    "transaction_date": row["transaction_date"],
                    "customer": row["customer"],
                    "product": row["product"],
                    "region": row["region"],
                    "issues": "; ".join(row_issues),
                }
            )

    return pd.DataFrame(issues)


def calculate_margin(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate gross margin dollars and gross margin percentage."""
    df = df.copy()

    df["gross_margin_dollars"] = df["revenue"] - df["cost_of_goods_sold"]

    df["gross_margin_pct"] = df.apply(
        lambda row: row["gross_margin_dollars"] / row["revenue"]
        if pd.notna(row["revenue"]) and row["revenue"] > 0
        else pd.NA,
        axis=1,
    )

    df["transaction_month"] = pd.to_datetime(df["transaction_date"]).dt.to_period("M").astype(str)

    return df


def create_margin_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Flag low-margin and negative-margin records."""
    flags = []

    for _, row in df.iterrows():
        flag_reasons = []

        if pd.notna(row["gross_margin_dollars"]) and row["gross_margin_dollars"] < 0:
            flag_reasons.append("Negative gross margin dollars")

        if pd.notna(row["gross_margin_pct"]) and row["gross_margin_pct"] < LOW_MARGIN_THRESHOLD:
            flag_reasons.append("Gross margin percentage below threshold")

        if flag_reasons:
            flags.append(
                {
                    "transaction_id": row["transaction_id"],
                    "transaction_date": row["transaction_date"],
                    "customer": row["customer"],
                    "product": row["product"],
                    "region": row["region"],
                    "revenue": row["revenue"],
                    "cost_of_goods_sold": row["cost_of_goods_sold"],
                    "gross_margin_dollars": row["gross_margin_dollars"],
                    "gross_margin_pct": row["gross_margin_pct"],
                    "flag_reasons": "; ".join(flag_reasons),
                }
            )

    return pd.DataFrame(flags)


def summarize_margin(df: pd.DataFrame, group_field: str) -> pd.DataFrame:
    """Summarize average gross margin by a selected business dimension."""
    summary = (
        df.groupby(group_field, dropna=False)
        .agg(
            transaction_count=("transaction_id", "count"),
            total_revenue=("revenue", "sum"),
            total_cost_of_goods_sold=("cost_of_goods_sold", "sum"),
            total_gross_margin_dollars=("gross_margin_dollars", "sum"),
            average_gross_margin_pct=("gross_margin_pct", "mean"),
        )
        .reset_index()
    )

    return summary


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    raw_df = load_data(DATA_PATH)

    data_quality_issues = validate_data(raw_df)
    margin_df = calculate_margin(raw_df)
    margin_flags = create_margin_flags(margin_df)

    product_summary = summarize_margin(margin_df, "product")
    customer_summary = summarize_margin(margin_df, "customer")
    region_summary = summarize_margin(margin_df, "region")
    month_summary = summarize_margin(margin_df, "transaction_month")

    gross_margin_summary = pd.concat(
        [
            product_summary.assign(summary_level="product").rename(columns={"product": "summary_value"}),
            customer_summary.assign(summary_level="customer").rename(columns={"customer": "summary_value"}),
            region_summary.assign(summary_level="region").rename(columns={"region": "summary_value"}),
            month_summary.assign(summary_level="month").rename(columns={"transaction_month": "summary_value"}),
        ],
        ignore_index=True,
    )

    gross_margin_summary = gross_margin_summary[
        [
            "summary_level",
            "summary_value",
            "transaction_count",
            "total_revenue",
            "total_cost_of_goods_sold",
            "total_gross_margin_dollars",
            "average_gross_margin_pct",
        ]
    ]

    margin_df.to_csv(OUTPUT_DIR / "margin_detail.csv", index=False)
    gross_margin_summary.to_csv(OUTPUT_DIR / "gross_margin_summary.csv", index=False)
    data_quality_issues.to_csv(OUTPUT_DIR / "data_quality_issues.csv", index=False)
    margin_flags.to_csv(OUTPUT_DIR / "margin_flags.csv", index=False)

    print("Avg Gross Margin analysis complete.")
    print(f"Rows processed: {len(raw_df)}")
    print(f"Data quality issue rows: {len(data_quality_issues)}")
    print(f"Margin flag rows: {len(margin_flags)}")
    print(f"Outputs written to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
