from __future__ import annotations

import pandas as pd


def hourly_sales(df: pd.DataFrame) -> pd.DataFrame:
	result = (
		df.groupby("hour_of_day", as_index=False)
		.agg(transactions=("money", "size"), revenue=("money", "sum"))
		.sort_values("hour_of_day")
	)
	return result.reset_index(drop=True)


def revenue_by_weekday(df: pd.DataFrame) -> pd.DataFrame:
	result = (
		df.groupby(["Weekdaysort", "Weekday"], as_index=False)["money"]
		.sum()
		.rename(columns={"money": "revenue"})
		.sort_values("Weekdaysort")
	)
	return result.reset_index(drop=True)


def revenue_by_month(df: pd.DataFrame) -> pd.DataFrame:
	result = (
		df.groupby(["Monthsort", "Month_name"], as_index=False)["money"]
		.sum()
		.rename(columns={"money": "revenue"})
		.sort_values("Monthsort")
	)
	return result.reset_index(drop=True)


def peak_weekday_hour(df: pd.DataFrame) -> pd.DataFrame:
	result = (
		df.groupby(["Weekday", "hour_of_day"], as_index=False)
		.agg(transactions=("money", "size"), revenue=("money", "sum"))
		.sort_values(["revenue", "transactions"], ascending=[False, False])
	)
	return result.reset_index(drop=True)
