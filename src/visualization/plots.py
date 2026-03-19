from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure


def plot_hourly_revenue(hourly_df: pd.DataFrame) -> Figure:
	fig, ax = plt.subplots(figsize=(10, 5))
	sns.barplot(data=hourly_df, x="hour_of_day", y="revenue", ax=ax, color="#4e79a7")
	ax.set_title("Revenue by Hour")
	ax.set_xlabel("Hour of Day")
	ax.set_ylabel("Revenue")
	fig.tight_layout()
	return fig


def plot_weekday_revenue(weekday_df: pd.DataFrame) -> Figure:
	fig, ax = plt.subplots(figsize=(9, 5))
	sns.barplot(data=weekday_df, x="Weekday", y="revenue", ax=ax, color="#f28e2b")
	ax.set_title("Revenue by Weekday")
	ax.set_xlabel("Weekday")
	ax.set_ylabel("Revenue")
	fig.tight_layout()
	return fig


def plot_monthly_revenue(month_df: pd.DataFrame) -> Figure:
	fig, ax = plt.subplots(figsize=(10, 5))
	sns.lineplot(data=month_df, x="Month_name", y="revenue", marker="o", ax=ax, color="#e15759")
	ax.set_title("Monthly Revenue Trend")
	ax.set_xlabel("Month")
	ax.set_ylabel("Revenue")
	fig.tight_layout()
	return fig


def plot_top_products(top_products_df: pd.DataFrame, value_column: str = "quantity") -> Figure:
	fig, ax = plt.subplots(figsize=(10, 6))
	sns.barplot(data=top_products_df, y="coffee_name", x=value_column, ax=ax, color="#59a14f")
	ax.set_title(f"Top Products by {value_column.replace('_', ' ').title()}")
	ax.set_xlabel(value_column.replace("_", " ").title())
	ax.set_ylabel("Coffee")
	fig.tight_layout()
	return fig


def plot_payment_distribution(payment_usage_df: pd.DataFrame) -> Figure:
	fig, ax = plt.subplots(figsize=(8, 5))
	sns.barplot(data=payment_usage_df, x="cash_type", y="transactions", ax=ax, color="#76b7b2")
	ax.set_title("Payment Method Distribution")
	ax.set_xlabel("Payment Method")
	ax.set_ylabel("Transactions")
	fig.tight_layout()
	return fig


def plot_payment_by_time_of_day(payment_tod_df: pd.DataFrame) -> Figure:
	pivot = payment_tod_df.pivot_table(
		index="Time_of_Day",
		columns="cash_type",
		values="transactions",
		aggfunc="sum",
		fill_value=0,
	)
	fig, ax = plt.subplots(figsize=(9, 5))
	pivot.plot(kind="bar", stacked=True, ax=ax, colormap="Set2")
	ax.set_title("Payment Method by Time of Day")
	ax.set_xlabel("Time of Day")
	ax.set_ylabel("Transactions")
	ax.legend(title="Payment Method", bbox_to_anchor=(1.02, 1), loc="upper left")
	fig.tight_layout()
	return fig


def plot_hour_product_heatmap(df: pd.DataFrame) -> Figure:
	pivot = df.pivot_table(
		index="hour_of_day",
		columns="coffee_name",
		values="money",
		aggfunc="size",
		fill_value=0,
	)
	fig, ax = plt.subplots(figsize=(12, 6))
	sns.heatmap(pivot, cmap="YlGnBu", ax=ax)
	ax.set_title("Hour vs Product Heatmap (Transactions)")
	ax.set_xlabel("Coffee")
	ax.set_ylabel("Hour of Day")
	fig.tight_layout()
	return fig


def plot_time_product_heatmap(df: pd.DataFrame) -> Figure:
	pivot = df.pivot_table(
		index="Time_of_Day",
		columns="coffee_name",
		values="money",
		aggfunc="sum",
		fill_value=0.0,
	)
	fig, ax = plt.subplots(figsize=(12, 5))
	sns.heatmap(pivot, cmap="YlOrRd", ax=ax)
	ax.set_title("Time-of-Day Product Pattern (Revenue)")
	ax.set_xlabel("Coffee")
	ax.set_ylabel("Time of Day")
	fig.tight_layout()
	return fig
