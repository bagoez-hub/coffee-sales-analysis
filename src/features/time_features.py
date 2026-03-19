from __future__ import annotations

import pandas as pd


def _bucket_time_of_day(hour: float) -> str:
	if pd.isna(hour):
		return "Night"
	hour_int = int(hour)
	if 5 <= hour_int < 12:
		return "Morning"
	if 12 <= hour_int < 17:
		return "Afternoon"
	if 17 <= hour_int < 21:
		return "Evening"
	return "Night"


def derive_time_features(df: pd.DataFrame) -> pd.DataFrame:
	enriched = df.copy()

	timestamp = pd.to_datetime(
		enriched["Date"].astype(str) + " " + enriched["Time"].astype(str),
		errors="coerce",
	)
	enriched["transaction_datetime"] = timestamp

	if "hour_of_day" not in enriched.columns:
		enriched["hour_of_day"] = timestamp.dt.hour

	enriched["day_of_month"] = timestamp.dt.day
	enriched["week_of_year"] = timestamp.dt.isocalendar().week.astype("Int64")
	enriched["is_weekend"] = timestamp.dt.weekday >= 5
	enriched["weekday_number"] = timestamp.dt.weekday + 1
	enriched["month_number"] = timestamp.dt.month

	if "Time_of_Day" not in enriched.columns:
		enriched["Time_of_Day"] = enriched["hour_of_day"].map(_bucket_time_of_day)
	else:
		missing_tod = enriched["Time_of_Day"].isna() | (enriched["Time_of_Day"].astype(str).str.strip() == "")
		enriched.loc[missing_tod, "Time_of_Day"] = enriched.loc[missing_tod, "hour_of_day"].map(_bucket_time_of_day)

	return enriched
