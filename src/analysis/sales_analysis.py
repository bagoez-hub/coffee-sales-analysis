from __future__ import annotations

import pandas as pd


def sales_overview(df: pd.DataFrame) -> dict[str, float | int]:
	return {
		"transactions": int(df.shape[0]),
		"total_revenue": float(df["money"].sum()),
		"average_transaction_value": float(df["money"].mean()),
		"unique_products": int(df["coffee_name"].nunique()),
	}


def revenue_by_payment(df: pd.DataFrame) -> pd.DataFrame:
	result = (
		df.groupby("cash_type", as_index=False)["money"]
		.sum()
		.rename(columns={"money": "total_revenue"})
		.sort_values("total_revenue", ascending=False)
	)
	return result.reset_index(drop=True)


def average_ticket_by_payment(df: pd.DataFrame) -> pd.DataFrame:
	result = (
		df.groupby("cash_type", as_index=False)["money"]
		.mean()
		.rename(columns={"money": "avg_ticket"})
		.sort_values("avg_ticket", ascending=False)
	)
	return result.reset_index(drop=True)


def payment_method_usage(df: pd.DataFrame) -> pd.DataFrame:
	result = (
		df.groupby("cash_type", as_index=False)
		.agg(transactions=("money", "size"))
		.sort_values("transactions", ascending=False)
	)
	return result.reset_index(drop=True)


def payment_by_time_of_day(df: pd.DataFrame) -> pd.DataFrame:
	result = (
		df.groupby(["Time_of_Day", "cash_type"], as_index=False)
		.agg(transactions=("money", "size"), revenue=("money", "sum"))
	)
	return result.reset_index(drop=True)


def daily_revenue(df: pd.DataFrame) -> pd.DataFrame:
	result = (
		df.groupby("Date", as_index=False)["money"]
		.sum()
		.rename(columns={"money": "daily_revenue"})
		.sort_values("Date")
	)
	return result.reset_index(drop=True)
