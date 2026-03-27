from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from features.time_features import derive_time_features


def test_derive_time_features_adds_expected_columns() -> None:
	df = pd.DataFrame(
		{
			"Date": ["2024-03-09"],
			"Time": ["10:15:50"],
			"hour_of_day": [10],
			"Time_of_Day": ["Morning"],
			"money": [38.7],
			"coffee_name": ["Latte"],
		}
	)

	featured = derive_time_features(df)

	assert "transaction_datetime" in featured.columns
	assert "day_of_month" in featured.columns
	assert "week_of_year" in featured.columns
	assert "is_weekend" in featured.columns
	assert "weekday_number" in featured.columns
	assert "month_number" in featured.columns


def test_derive_time_features_sets_weekend_flag_correctly() -> None:
	df = pd.DataFrame(
		{
			"Date": ["2024-03-09", "2024-03-11"],
			"Time": ["10:00:00", "10:00:00"],
			"hour_of_day": [10, 10],
			"Time_of_Day": ["Morning", "Morning"],
			"money": [38.7, 28.9],
			"coffee_name": ["Latte", "Americano"],
		}
	)

	featured = derive_time_features(df)
	assert bool(featured.loc[0, "is_weekend"]) is True
	assert bool(featured.loc[1, "is_weekend"]) is False


def test_derive_time_features_fills_time_of_day_when_missing() -> None:
	df = pd.DataFrame(
		{
			"Date": ["2024-03-09"],
			"Time": ["18:30:00"],
			"hour_of_day": [18],
			"Time_of_Day": [""],
			"money": [38.7],
			"coffee_name": ["Latte"],
		}
	)

	featured = derive_time_features(df)
	assert featured.loc[0, "Time_of_Day"] == "Night"
