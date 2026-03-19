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
