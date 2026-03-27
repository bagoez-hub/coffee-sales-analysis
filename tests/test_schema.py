from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from validation.schema import assert_valid_dataset, is_valid_dataset, validate_dataset


def make_valid_df() -> pd.DataFrame:
	return pd.DataFrame(
		{
			"hour_of_day": [10, 12],
			"cash_type": ["card", "card"],
			"money": [38.7, 24.0],
			"coffee_name": ["Latte", "Espresso"],
			"Time_of_Day": ["Morning", "Afternoon"],
			"Weekday": ["Mon", "Tue"],
			"Month_name": ["Mar", "Mar"],
			"Weekdaysort": [1, 2],
			"Monthsort": [3, 3],
			"Date": ["2024-03-04", "2024-03-05"],
			"Time": ["10:15:50", "12:05:15"],
		}
	)


def test_validate_dataset_valid_input_has_no_errors() -> None:
	df = make_valid_df()
	report = validate_dataset(df)
	assert all(len(items) == 0 for items in report.values())
	assert is_valid_dataset(df)


def test_validate_dataset_detects_missing_required_column() -> None:
	df = make_valid_df().drop(columns=["money"])
	report = validate_dataset(df)
	assert report["structure"]
	assert not is_valid_dataset(df)


def test_assert_valid_dataset_raises_for_invalid_hour() -> None:
	df = make_valid_df()
	df.loc[0, "hour_of_day"] = 30

	with pytest.raises(ValueError):
		assert_valid_dataset(df)


def test_assert_valid_dataset_raises_for_negative_money() -> None:
	df = make_valid_df()
	df.loc[0, "money"] = -1

	with pytest.raises(ValueError):
		assert_valid_dataset(df)
