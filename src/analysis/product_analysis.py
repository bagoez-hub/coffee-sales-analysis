from __future__ import annotations

import pandas as pd


def top_products_by_volume(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
	result = (
		df.groupby("coffee_name", as_index=False)
		.agg(quantity=("coffee_name", "size"))
		.sort_values("quantity", ascending=False)
		.head(n)
	)
	return result.reset_index(drop=True)


def top_products_by_revenue(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
	result = (
		df.groupby("coffee_name", as_index=False)["money"]
		.sum()
		.rename(columns={"money": "revenue"})
		.sort_values("revenue", ascending=False)
		.head(n)
	)
	return result.reset_index(drop=True)


def best_product_per_time_of_day(df: pd.DataFrame) -> pd.DataFrame:
	grouped = (
		df.groupby(["Time_of_Day", "coffee_name"], as_index=False)
		.agg(quantity=("coffee_name", "size"), revenue=("money", "sum"))
		.sort_values(["Time_of_Day", "quantity", "revenue"], ascending=[True, False, False])
	)

	best = grouped.groupby("Time_of_Day", as_index=False).head(1)
	return best.reset_index(drop=True)


def average_ticket_by_product(df: pd.DataFrame) -> pd.DataFrame:
	result = (
		df.groupby("coffee_name", as_index=False)["money"]
		.mean()
		.rename(columns={"money": "avg_ticket"})
		.sort_values("avg_ticket", ascending=False)
	)
	return result.reset_index(drop=True)


def underperforming_products(df: pd.DataFrame) -> pd.DataFrame:
	revenue_per_product = (
		df.groupby("coffee_name", as_index=False)["money"]
		.sum()
		.rename(columns={"money": "revenue"})
	)
	avg_revenue = revenue_per_product["revenue"].mean()
	result = revenue_per_product[revenue_per_product["revenue"] < avg_revenue].copy()
	result["gap_to_avg"] = avg_revenue - result["revenue"]
	return result.sort_values("revenue").reset_index(drop=True)


def peak_product_per_hour(df: pd.DataFrame) -> pd.DataFrame:
	grouped = (
		df.groupby(["hour_of_day", "coffee_name"], as_index=False)
		.agg(transactions=("coffee_name", "size"))
		.sort_values(["hour_of_day", "transactions"], ascending=[True, False])
	)
	return grouped.groupby("hour_of_day", as_index=False).head(1).reset_index(drop=True)
