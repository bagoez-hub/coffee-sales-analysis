from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
	project_root: Path = Path(__file__).resolve().parents[1]
	raw_data_path: Path = project_root / "data" / "raw" / "Coffe_sales.csv"
	interim_data_dir: Path = project_root / "data" / "interim"
	processed_data_dir: Path = project_root / "data" / "processed"
	reports_dir: Path = project_root / "reports"
	figures_dir: Path = reports_dir / "figures"


REQUIRED_COLUMNS: tuple[str, ...] = (
	"hour_of_day",
	"cash_type",
	"money",
	"coffee_name",
	"Time_of_Day",
	"Weekday",
	"Month_name",
	"Weekdaysort",
	"Monthsort",
	"Date",
	"Time",
)

CRITICAL_COLUMNS: tuple[str, ...] = ("money", "coffee_name", "Date", "Time")

ALLOWED_TIME_OF_DAY: set[str] = {"Morning", "Afternoon", "Night"}

ALLOWED_CASH_TYPES: set[str] = {"card"}

ALLOWED_PRODUCTS: set[str] = {
	"Americano",
	"Americano with Milk",
	"Cappuccino",
	"Cocoa",
	"Cortado",
	"Espresso",
	"Hot Chocolate",
	"Latte",
}

ALLOWED_WEEKDAYS: set[str] = {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}

ALLOWED_MONTHS: set[str] = {
	"Jan",
	"Feb",
	"Mar",
	"Apr",
	"May",
	"Jun",
	"Jul",
	"Aug",
	"Sep",
	"Oct",
	"Nov",
	"Dec",
}

WEEKDAY_ORDER: tuple[str, ...] = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
MONTH_ORDER: tuple[str, ...] = (
	"Jan",
	"Feb",
	"Mar",
	"Apr",
	"May",
	"Jun",
	"Jul",
	"Aug",
	"Sep",
	"Oct",
	"Nov",
	"Dec",
)

settings = Settings()
