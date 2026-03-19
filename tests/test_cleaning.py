from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cleaning.clean_data import clean_sales_data


def test_clean_sales_data_strips_and_standardizes_values() -> None:
	df = pd.DataFrame(
		{
			"hour_of_day": ["10"],
			"cash_type": [" card "],
			"money": ["38.7"],
			"coffee_name": [" Latte "],
			"Time_of_Day": ["Morning"],
			"Weekday": [" Mon "],
			"Month_name": [" Mar "],
			"Weekdaysort": ["1"],
			"Monthsort": ["3"],
			"Date": ["2024-03-04"],
			"Time": ["10:15:50.520000"],
		}
	)

	cleaned = clean_sales_data(df)

	assert cleaned.loc[0, "cash_type"] == "card"
	assert cleaned.loc[0, "coffee_name"] == "Latte"
	assert cleaned.loc[0, "money"] == 38.7
	assert cleaned.loc[0, "Time"] == "10:15:50"


def test_clean_sales_data_removes_invalid_critical_rows() -> None:
	df = pd.DataFrame(
		{
			"hour_of_day": [10, 11],
			"cash_type": ["card", "card"],
			"money": [28.9, None],
			"coffee_name": ["Americano", "Latte"],
			"Time_of_Day": ["Morning", "Morning"],
			"Weekday": ["Mon", "Mon"],
			"Month_name": ["Mar", "Mar"],
			"Weekdaysort": [1, 1],
			"Monthsort": [3, 3],
			"Date": ["2024-03-04", "2024-03-04"],
			"Time": ["10:00:00", "11:00:00"],
		}
	)

	cleaned = clean_sales_data(df)
	assert cleaned.shape[0] == 1
	assert cleaned.iloc[0]["coffee_name"] == "Americano"


def test_clean_sales_data_drops_duplicates() -> None:
	row = {
		"hour_of_day": 10,
		"cash_type": "card",
		"money": 28.9,
		"coffee_name": "Americano",
		"Time_of_Day": "Morning",
		"Weekday": "Mon",
		"Month_name": "Mar",
		"Weekdaysort": 1,
		"Monthsort": 3,
		"Date": "2024-03-04",
		"Time": "10:00:00",
	}
	df = pd.DataFrame([row, row])

	cleaned = clean_sales_data(df)
	assert cleaned.shape[0] == 1
