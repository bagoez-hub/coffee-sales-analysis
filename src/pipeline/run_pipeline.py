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
	logger.info("Pipeline started")
	raw_df = load_raw_sales_data(input_path)
	logger.info(f"Loaded {raw_df.shape[0]} raw rows from source")

	assert_valid_dataset(raw_df)
	logger.info("Dataset validation passed")

	cleaned_df = clean_sales_data(raw_df)
	logger.info(f"Cleaning complete — {cleaned_df.shape[0]} rows retained")

	featured_df = derive_time_features(cleaned_df)
	logger.info("Time features derived")

	overview = sales_overview(featured_df)

	output_path = Path(output_dir) if output_dir is not None else settings.processed_data_dir
	output_path.mkdir(parents=True, exist_ok=True)

	processed_csv = output_path / "coffee_sales_processed.csv"
	report_json = output_path / "pipeline_report.json"

	featured_df.to_csv(processed_csv, index=False)
	logger.info(f"Processed data saved to {processed_csv}")

	report = {
		"rows_raw": int(raw_df.shape[0]),
		"rows_processed": int(featured_df.shape[0]),
		"processed_csv": str(processed_csv),
		"summary": overview,
	}

	report_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
	logger.info(f"Pipeline report written to {report_json}")
	logger.info("Pipeline complete")
	return report


if __name__ == "__main__":
	pipeline_report = run_pipeline()
	print(json.dumps(pipeline_report, indent=2))
