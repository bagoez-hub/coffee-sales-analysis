from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt

from analysis.product_analysis import top_products_by_revenue, top_products_by_volume
from analysis.sales_analysis import (
    average_ticket_by_payment,
    payment_by_time_of_day,
    payment_method_usage,
    revenue_by_payment,
    sales_overview,
)
from analysis.time_analysis import hourly_sales, revenue_by_month, revenue_by_weekday
from cleaning.clean_data import clean_sales_data
from config import settings
from features.time_features import derive_time_features
from ingestion.load_data import load_raw_sales_data
from validation.schema import assert_valid_dataset
from visualization.plots import (
    plot_hour_product_heatmap,
    plot_hourly_revenue,
    plot_monthly_revenue,
    plot_payment_by_time_of_day,
    plot_payment_distribution,
    plot_time_product_heatmap,
    plot_top_products,
    plot_weekday_revenue,
)


def _save_figure(path: Path, figure: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(figure)


def run_full_pipeline(input_csv: str | None = None, top_n_products: int = 10) -> dict[str, Any]:
    raw_df = load_raw_sales_data(input_csv)
    assert_valid_dataset(raw_df)

    clean_df = clean_sales_data(raw_df)
    feature_df = derive_time_features(clean_df)

    processed_dir = settings.processed_data_dir
    processed_dir.mkdir(parents=True, exist_ok=True)
    settings.figures_dir.mkdir(parents=True, exist_ok=True)

    processed_csv = processed_dir / "coffee_sales_processed.csv"
    feature_df.to_csv(processed_csv, index=False)

    hourly_df = hourly_sales(feature_df)
    weekday_df = revenue_by_weekday(feature_df)
    month_df = revenue_by_month(feature_df)
    top_volume_df = top_products_by_volume(feature_df, n=top_n_products)
    top_revenue_df = top_products_by_revenue(feature_df, n=top_n_products)
    payment_revenue_df = revenue_by_payment(feature_df)
    payment_avg_ticket_df = average_ticket_by_payment(feature_df)
    payment_usage_df = payment_method_usage(feature_df)
    payment_tod_df = payment_by_time_of_day(feature_df)

    hourly_df.to_csv(processed_dir / "hourly_sales.csv", index=False)
    weekday_df.to_csv(processed_dir / "weekday_revenue.csv", index=False)
    month_df.to_csv(processed_dir / "monthly_revenue.csv", index=False)
    top_volume_df.to_csv(processed_dir / "top_products_by_volume.csv", index=False)
    top_revenue_df.to_csv(processed_dir / "top_products_by_revenue.csv", index=False)
    payment_revenue_df.to_csv(processed_dir / "payment_revenue.csv", index=False)
    payment_avg_ticket_df.to_csv(processed_dir / "payment_avg_ticket.csv", index=False)
    payment_usage_df.to_csv(processed_dir / "payment_method_usage.csv", index=False)
    payment_tod_df.to_csv(processed_dir / "payment_by_time_of_day.csv", index=False)

    hourly_fig = plot_hourly_revenue(hourly_df)
    weekday_fig = plot_weekday_revenue(weekday_df)
    month_fig = plot_monthly_revenue(month_df)
    top_products_fig = plot_top_products(top_volume_df, value_column="quantity")
    top_revenue_fig = plot_top_products(top_revenue_df, value_column="revenue")
    payment_distribution_fig = plot_payment_distribution(payment_usage_df)
    payment_tod_fig = plot_payment_by_time_of_day(payment_tod_df)
    hour_product_heatmap_fig = plot_hour_product_heatmap(feature_df)
    time_product_heatmap_fig = plot_time_product_heatmap(feature_df)

    _save_figure(settings.figures_dir / "hourly_revenue.png", hourly_fig)
    _save_figure(settings.figures_dir / "weekday_revenue.png", weekday_fig)
    _save_figure(settings.figures_dir / "monthly_revenue_trend.png", month_fig)
    _save_figure(settings.figures_dir / "top_products_volume.png", top_products_fig)
    _save_figure(settings.figures_dir / "top_products_revenue.png", top_revenue_fig)
    _save_figure(settings.figures_dir / "payment_method_distribution.png", payment_distribution_fig)
    _save_figure(settings.figures_dir / "payment_by_time_of_day.png", payment_tod_fig)
    _save_figure(settings.figures_dir / "hour_product_heatmap.png", hour_product_heatmap_fig)
    _save_figure(settings.figures_dir / "time_product_heatmap.png", time_product_heatmap_fig)

    overview = sales_overview(feature_df)
    report = {
        "input_rows": int(raw_df.shape[0]),
        "processed_rows": int(feature_df.shape[0]),
        "processed_csv": str(processed_csv),
        "figures": [
            str(settings.figures_dir / "hourly_revenue.png"),
            str(settings.figures_dir / "weekday_revenue.png"),
            str(settings.figures_dir / "monthly_revenue_trend.png"),
            str(settings.figures_dir / "top_products_volume.png"),
            str(settings.figures_dir / "top_products_revenue.png"),
            str(settings.figures_dir / "payment_method_distribution.png"),
            str(settings.figures_dir / "payment_by_time_of_day.png"),
            str(settings.figures_dir / "hour_product_heatmap.png"),
            str(settings.figures_dir / "time_product_heatmap.png"),
        ],
        "summary": overview,
    }

    report_path = processed_dir / "pipeline_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run coffee sales analysis pipeline")
    parser.add_argument("--input-csv", default=None, help="Optional path to raw CSV input")
    parser.add_argument("--top-n-products", type=int, default=10, help="Top N products for product reports")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = run_full_pipeline(input_csv=args.input_csv, top_n_products=args.top_n_products)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
