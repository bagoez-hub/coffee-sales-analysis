from __future__ import annotations

from pathlib import Path

import pandas as pd

from config import settings


def load_raw_sales_data(csv_path: str | Path | None = None) -> pd.DataFrame:
	path = Path(csv_path) if csv_path is not None else settings.raw_data_path
	if not path.exists():
		raise FileNotFoundError(f"Raw data file not found: {path}")
	return pd.read_csv(path)
