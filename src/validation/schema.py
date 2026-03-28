from __future__ import annotations

from typing import Any

import pandas as pd

from config import (
    ALLOWED_CASH_TYPES,
    ALLOWED_PRODUCTS,
    ALLOWED_TIME_OF_DAY,
    CRITICAL_COLUMNS,
    MONTH_ORDER,
    REQUIRED_COLUMNS,
    WEEKDAY_ORDER,
)


def _parse_time_series(series: pd.Series) -> pd.Series:
	parsed_time = pd.to_datetime(series, format="%H:%M:%S.%f", errors="coerce")
	missing_mask = parsed_time.isna()
	if missing_mask.any():
		parsed_time.loc[missing_mask] = pd.to_datetime(
			series.loc[missing_mask],
			format="%H:%M:%S",
			errors="coerce",
		)
	return parsed_time


def _validate_structure(df: pd.DataFrame) -> list[str]:
	errors: list[str] = []
	if df.shape[0] == 0:
		errors.append("Dataset must contain at least one row")
	missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
	if missing:
		errors.append(f"Missing required columns: {missing}")

	duplicate_cols = df.columns[df.columns.duplicated()].tolist()
	if duplicate_cols:
		errors.append(f"Duplicate column names detected: {duplicate_cols}")
	return errors


def _validate_missing_values(df: pd.DataFrame) -> list[str]:
	errors: list[str] = []
	for col in CRITICAL_COLUMNS:
		if col in df.columns and df[col].isna().any():
			errors.append(f"Critical column '{col}' contains null values")
	return errors


def _validate_value_ranges(df: pd.DataFrame) -> list[str]:
	errors: list[str] = []

	if "hour_of_day" in df.columns:
		hours = pd.to_numeric(df["hour_of_day"], errors="coerce")
		if hours.isna().any() or not hours.dropna().between(6, 22).all():
			errors.append("hour_of_day must be numeric and between 6 and 22")

	if "money" in df.columns:
		money = pd.to_numeric(df["money"], errors="coerce")
		if money.isna().any() or (money < 0).any():
			errors.append("money must be numeric and greater than or equal to 0")

	if "Weekdaysort" in df.columns:
		weekday_sort = pd.to_numeric(df["Weekdaysort"], errors="coerce")
		if weekday_sort.isna().any() or not weekday_sort.dropna().between(1, 7).all():
			errors.append("Weekdaysort must be numeric and between 1 and 7")

	if "Monthsort" in df.columns:
		month_sort = pd.to_numeric(df["Monthsort"], errors="coerce")
		if month_sort.isna().any() or not month_sort.dropna().between(1, 12).all():
			errors.append("Monthsort must be numeric and between 1 and 12")

	if "Time_of_Day" in df.columns:
		invalid_tod = sorted(set(df["Time_of_Day"].dropna().astype(str)) - ALLOWED_TIME_OF_DAY)
		if invalid_tod:
			errors.append(f"Time_of_Day has invalid values: {invalid_tod}")

	if "cash_type" in df.columns:
		invalid_cash = sorted(set(df["cash_type"].dropna().astype(str)) - ALLOWED_CASH_TYPES)
		if invalid_cash:
			errors.append(f"cash_type has unrecognised values: {invalid_cash}")

	if "coffee_name" in df.columns:
		invalid_products = sorted(set(df["coffee_name"].dropna().astype(str)) - ALLOWED_PRODUCTS)
		if invalid_products:
			errors.append(f"coffee_name has unknown products: {invalid_products}")

	if "Weekday" in df.columns:
		invalid_weekdays = sorted(set(df["Weekday"].dropna().astype(str)) - set(WEEKDAY_ORDER))
		if invalid_weekdays:
			errors.append(f"Weekday has invalid values: {invalid_weekdays}")

	if "Month_name" in df.columns:
		invalid_months = sorted(set(df["Month_name"].dropna().astype(str)) - set(MONTH_ORDER))
		if invalid_months:
			errors.append(f"Month_name has invalid values: {invalid_months}")

	if "Date" in df.columns:
		parsed_date = pd.to_datetime(df["Date"], errors="coerce")
		if parsed_date.isna().any():
			errors.append("Date contains invalid values")

	if "Time" in df.columns:
		parsed_time = _parse_time_series(df["Time"])
		if parsed_time.isna().any():
			errors.append("Time contains invalid values")

	return errors


def validate_dataset(df: pd.DataFrame) -> dict[str, list[str]]:
	report = {
		"structure": _validate_structure(df),
		"missing": _validate_missing_values(df),
		"values": _validate_value_ranges(df),
	}
	return report


def is_valid_dataset(df: pd.DataFrame) -> bool:
	report = validate_dataset(df)
	return all(len(items) == 0 for items in report.values())


def assert_valid_dataset(df: pd.DataFrame) -> None:
	report = validate_dataset(df)
	all_errors = [message for group in report.values() for message in group]
	if all_errors:
		message = "\n".join(f"- {err}" for err in all_errors)
		raise ValueError(f"Dataset validation failed:\n{message}")


def summarize_validation(df: pd.DataFrame) -> dict[str, Any]:
	report = validate_dataset(df)
	all_errors = [message for group in report.values() for message in group]
	return {
		"rows": int(df.shape[0]),
		"columns": int(df.shape[1]),
		"is_valid": len(all_errors) == 0,
		"errors": all_errors,
	}
