from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from loguru import logger

from analysis.sales_analysis import sales_overview
from cleaning.clean_data import clean_sales_data
from config import settings
from features.time_features import derive_time_features
from ingestion.load_data import load_raw_sales_data
from validation.schema import assert_valid_dataset


def run_pipeline(input_path: str | Path | None = None, output_dir: str | Path | None = None) -> dict[str, Any]:
	logger.info("Loading and validating raw data")
	raw_df = load_raw_sales_data(input_path)
	assert_valid_dataset(raw_df)

	logger.info("Cleaning data and deriving features")
	cleaned_df = clean_sales_data(raw_df)
	featured_df = derive_time_features(cleaned_df)
	overview = sales_overview(featured_df)

	output_path = Path(output_dir) if output_dir is not None else settings.processed_data_dir
	output_path.mkdir(parents=True, exist_ok=True)

	processed_csv = output_path / "coffee_sales_processed.csv"
	report_json = output_path / "pipeline_report.json"

	featured_df.to_csv(processed_csv, index=False)

	report = {
		"rows_raw": int(raw_df.shape[0]),
		"rows_processed": int(featured_df.shape[0]),
		"processed_csv": str(processed_csv),
		"summary": overview,
	}

	report_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
	logger.info("Pipeline report saved to {}", report_json)
	return report


if __name__ == "__main__":
	pipeline_report = run_pipeline()
	logger.info("Pipeline report:\n{}", json.dumps(pipeline_report, indent=2))
