from __future__ import annotations

import pandas as pd

from config import ALLOWED_TIME_OF_DAY, CRITICAL_COLUMNS


def _bucket_time_of_day(hour: float) -> str:
	if pd.isna(hour):
		return "Night"
	hour_int = int(hour)
	if 5 <= hour_int < 12:
		return "Morning"
	if 12 <= hour_int < 17:
		return "Afternoon"
	return "Night"


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


def clean_sales_data(df: pd.DataFrame, drop_duplicates: bool = True) -> pd.DataFrame:
	cleaned = df.copy()
	cleaned.columns = [str(col).strip() for col in cleaned.columns]

	for col in ["cash_type", "coffee_name", "Time_of_Day", "Weekday", "Month_name", "Date", "Time"]:
		if col in cleaned.columns:
			cleaned[col] = cleaned[col].astype(str).str.strip()

	if "money" in cleaned.columns:
		cleaned["money"] = pd.to_numeric(cleaned["money"], errors="coerce")

	if "hour_of_day" in cleaned.columns:
		cleaned["hour_of_day"] = pd.to_numeric(cleaned["hour_of_day"], errors="coerce")

	if "Weekdaysort" in cleaned.columns:
		cleaned["Weekdaysort"] = pd.to_numeric(cleaned["Weekdaysort"], errors="coerce")

	if "Monthsort" in cleaned.columns:
		cleaned["Monthsort"] = pd.to_numeric(cleaned["Monthsort"], errors="coerce")

	if "Date" in cleaned.columns:
		cleaned["Date"] = pd.to_datetime(cleaned["Date"], errors="coerce").dt.date

	if "Time" in cleaned.columns:
		parsed_time = _parse_time_series(cleaned["Time"])
		cleaned["Time"] = parsed_time.dt.strftime("%H:%M:%S")

	if "Time_of_Day" in cleaned.columns:
		invalid_tod_mask = ~cleaned["Time_of_Day"].isin(ALLOWED_TIME_OF_DAY)
		if "hour_of_day" in cleaned.columns:
			cleaned.loc[invalid_tod_mask, "Time_of_Day"] = cleaned.loc[invalid_tod_mask, "hour_of_day"].map(
				_bucket_time_of_day
			)

	if "Weekdaysort" in cleaned.columns and "Date" in cleaned.columns:
		date_series = pd.to_datetime(cleaned["Date"], errors="coerce")
		cleaned["Weekdaysort"] = cleaned["Weekdaysort"].fillna(date_series.dt.weekday + 1)

	if "Monthsort" in cleaned.columns and "Date" in cleaned.columns:
		date_series = pd.to_datetime(cleaned["Date"], errors="coerce")
		cleaned["Monthsort"] = cleaned["Monthsort"].fillna(date_series.dt.month)

	if "Weekday" in cleaned.columns and "Date" in cleaned.columns:
		date_series = pd.to_datetime(cleaned["Date"], errors="coerce")
		missing_weekday = cleaned["Weekday"].isna() | (cleaned["Weekday"] == "")
		cleaned.loc[missing_weekday, "Weekday"] = date_series.dt.strftime("%a")

	if "Month_name" in cleaned.columns and "Date" in cleaned.columns:
		date_series = pd.to_datetime(cleaned["Date"], errors="coerce")
		missing_month = cleaned["Month_name"].isna() | (cleaned["Month_name"] == "")
		cleaned.loc[missing_month, "Month_name"] = date_series.dt.strftime("%b")

	for col in CRITICAL_COLUMNS:
		if col in cleaned.columns:
			cleaned = cleaned[cleaned[col].notna()]

	if "money" in cleaned.columns:
		cleaned = cleaned[cleaned["money"] >= 0]

	if drop_duplicates:
		cleaned = cleaned.drop_duplicates()

	sort_columns = [col for col in ["Date", "Time"] if col in cleaned.columns]
	if sort_columns:
		cleaned = cleaned.sort_values(sort_columns)

	return cleaned.reset_index(drop=True)
