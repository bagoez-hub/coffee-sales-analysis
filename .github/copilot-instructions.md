# Coffee Sales Analysis — Copilot Instructions

---

## 1. Project Overview

**Project name:** Coffee Sales Analysis

This project analyzes a real-world transactional coffee shop sales dataset. The dataset covers **3,547 individual purchase transactions** recorded between **2024-03-01 and 2025-03-23** (approximately one year), spanning **381 unique trading days**.

Each row represents a single sale transaction and includes the product purchased, the revenue generated, the exact timestamp, and derived time-dimension columns such as hour bucket, weekday, and month.

### Dataset File

* File: `data/raw/Coffe_sales.csv`
* Rows: 3,547 transactions
* Columns: 11
* Date range: 2024-03-01 → 2025-03-23

### Dataset Column Reference

| Column       | Meaning                                       | Actual Values / Format                          | Notes                                            |
| ------------ | --------------------------------------------- | ----------------------------------------------- | ------------------------------------------------ |
| hour\_of\_day | Hour when the transaction occurred            | Integer, range 6–22 (no overnight transactions) | Enables hourly sales analysis                    |
| cash\_type   | Payment method used                           | `card` (only value present in dataset)          | Dataset contains card-only transactions          |
| money        | Transaction value in currency units           | Float, range 18.12–38.70                        | Represents revenue; prices are fixed per product |
| coffee\_name | Product purchased                             | See product list below                          | 8 distinct products                              |
| Time\_of\_Day | Categorized time bucket                       | `Morning` / `Afternoon` / `Night`               | No "Evening" bucket exists in this dataset       |
| Weekday      | Abbreviated day name                          | `Mon` `Tue` `Wed` `Thu` `Fri` `Sat` `Sun`       | 3-letter abbreviation, not full name             |
| Month\_name  | Abbreviated month name                        | `Jan` `Feb` `Mar` … `Dec`                       | 3-letter abbreviation, not full name             |
| Weekdaysort  | Numeric weekday sort order                    | Integer 1–7                                     | Use for correct chronological chart ordering     |
| Monthsort    | Numeric month sort order                      | Integer 1–12                                    | Prevents alphabetical month sorting issues       |
| Date         | Calendar date (ISO format)                    | `YYYY-MM-DD`                                    | Enables daily aggregation                        |
| Time         | Exact transaction timestamp                   | `HH:MM:SS.ffffff`                               | Can be combined with Date for full timestamp     |

### Known Products (`coffee_name`)

* Americano
* Americano with Milk
* Cappuccino
* Cocoa
* Cortado
* Espresso
* Hot Chocolate
* Latte

---

## 2. Analysis Purposes

The primary purpose of this analysis is to extract business intelligence from coffee shop transaction data. The analysis is designed to support decision-making in the following areas:

**Operational planning**
Identify peak trading hours and days so staffing levels, inventory, and preparation can be optimized.

**Product strategy**
Understand which products sell the most by volume and which generate the most revenue. Identify which products are popular during specific time periods.

**Revenue understanding**
Track how revenue is distributed across hours, weekdays, and months. Identify seasonal trends.

**Customer behavior modeling**
Understand customer purchase patterns — when they buy, what they buy, and how timing affects product preference.

**Reproducible reporting**
Produce clean, validated, and documented analysis that can be re-run as new data arrives, generating consistent and comparable results.

---

## 3. Tech Stack

| Layer              | Tool / Library         | Purpose                                         |
| ------------------ | ---------------------- | ----------------------------------------------- |
| Language           | Python ≥ 3.14          | Core programming language                       |
| Data manipulation  | pandas ≥ 2.2.0         | DataFrame operations, aggregations, cleaning    |
| Numerical compute  | numpy ≥ 1.26.0         | Array operations, statistical calculations      |
| Static plotting    | matplotlib ≥ 3.8.0     | Charts and figures for reports                  |
| Statistical plots  | seaborn ≥ 0.13.0       | Heatmaps, distribution plots, categorical charts|
| Interactive plots  | plotly ≥ 5.24.0        | Interactive charts for notebook exploration     |
| Data validation    | pydantic ≥ 2.8.0       | Schema validation of dataset structure          |
| Outlier detection  | scikit-learn ≥ 1.5.0   | Statistical outlier detection in `money` column |
| Date parsing       | python-dateutil ≥ 2.9.0| Robust date and time parsing utilities          |
| Logging            | loguru ≥ 0.7.0         | Structured pipeline logging                     |
| Notebooks          | jupyter ≥ 1.1.0        | Interactive analysis documentation              |
| Notebook kernel    | ipykernel ≥ 6.29.0     | Jupyter kernel for Python execution             |
| Testing            | pytest ≥ 8.3.0         | Unit and integration test runner                |
| Test coverage      | pytest-cov ≥ 5.0.0     | Test coverage measurement and reporting         |
| Code formatting    | black ≥ 24.8.0         | Automatic code formatting                       |
| Linting            | ruff ≥ 0.6.0           | Fast linting and import sorting                 |
| Build system       | setuptools ≥ 68, wheel | Package build backend                           |

---

## 4. Dependencies

All runtime and development dependencies are declared in `pyproject.toml`.

### Runtime Dependencies

```
pandas>=2.2.0
matplotlib>=3.8.0
seaborn>=0.13.0
plotly>=5.24.0
numpy>=1.26.0
scikit-learn>=1.5.0
python-dateutil>=2.9.0
pydantic>=2.8.0
jupyter>=1.1.0
ipykernel>=6.29.0
loguru>=0.7.0
```

### Development Dependencies

```
pytest>=8.3.0
pytest-cov>=5.0.0
black>=24.8.0
ruff>=0.6.0
```

### Installation

```bash
pip install -e .
pip install -e ".[dev]"
```

---

## 5. Folder Structure

```
coffee-sales-analysis/
│
├── pyproject.toml          # Project config, dependencies, tool settings
├── README.md
├── main.py                 # Entry point for running the full pipeline
│
├── data/
│   ├── raw/                # Original unmodified source data
│   │   └── Coffe_sales.csv
│   ├── interim/            # Partially cleaned or transformed data
│   ├── processed/          # Final cleaned data ready for analysis
│   └── external/           # Reference data from external sources
│
├── notebooks/
│   ├── 01_eda.ipynb        # Exploratory data analysis
│   ├── 02_cleaning.ipynb   # Data cleaning walkthrough
│   └── 03_analysis.ipynb   # Business insights and visualizations
│
├── src/
│   ├── __init__.py
│   ├── config.py           # Shared configuration and constants
│   │
│   ├── ingestion/
│   │   └── load_data.py    # CSV loading and initial parsing
│   │
│   ├── validation/
│   │   └── schema.py       # Pydantic schema and validation rules
│   │
│   ├── cleaning/
│   │   └── clean_data.py   # Data cleaning and imputation logic
│   │
│   ├── features/
│   │   └── time_features.py # Time dimension feature engineering
│   │
│   ├── analysis/
│   │   ├── sales_analysis.py   # Revenue and transaction aggregations
│   │   ├── time_analysis.py    # Hourly, daily, monthly breakdowns
│   │   └── product_analysis.py # Product performance analysis
│   │
│   ├── visualization/
│   │   └── plots.py        # Reusable chart functions
│   │
│   └── pipeline/
│       └── run_pipeline.py # Orchestrates the full analysis pipeline
│
├── tests/
│   ├── __init__.py
│   ├── test_schema.py      # Tests for validation rules
│   ├── test_cleaning.py    # Tests for cleaning functions
│   └── test_features.py    # Tests for feature engineering
│
└── reports/
    ├── figures/            # Exported chart images
    └── summary.md          # Written summary of findings
```

---

## 6. Code Writing Rules

All source code in `src/` and `tests/` must follow these rules.

### Style and Formatting

* **Formatter:** `black` with `line-length = 120` and `target-version = py314`
* **Linter:** `ruff` with the same line length; rules `E, F, W, I, B, UP, N` are enforced
* **Quotes:** Do not normalize string quotes (black `skip-string-normalization = true`)
* **Trailing commas:** Do not add magic trailing commas (`skip-magic-trailing-comma = true`)
* **Imports:** Always sort imports (ruff rule `I`); standard library first, then third-party, then local

### Code Structure Rules

* All reusable logic must live in `src/` — notebooks call `src/` functions, they do not contain raw logic
* Each module has a single, clearly defined responsibility (ingestion, validation, cleaning, features, analysis, visualization, pipeline)
* Use type hints on all function signatures
* Use `loguru` for logging in pipeline and processing modules — do not use `print()` for operational messages
* Configuration values (file paths, constants, column names) must be defined in `src/config.py`, not hardcoded in modules
* Do not use wildcard imports (`from module import *`)

### Testing Rules

* All functions in `src/` must have corresponding tests in `tests/`
* Tests are run with `pytest` and coverage is reported with `pytest-cov`
* Minimum test coverage target: 80%
* Run tests with: `pytest`

---

## 7. Code Validation Rules

Data validation ensures the dataset is reliable before any analysis begins. Validation is implemented in `src/validation/schema.py` using Pydantic.

### Structural Validation

* Dataset must contain all 11 required columns (listed below)
* No duplicate column names permitted
* Row count must be > 0

**Required columns:**

```
hour_of_day, cash_type, money, coffee_name, Time_of_Day,
Weekday, Month_name, Weekdaysort, Monthsort, Date, Time
```

### Type Validation

| Column       | Expected Type    |
| ------------ | ---------------- |
| hour\_of\_day | integer          |
| cash\_type   | string/category  |
| money        | float            |
| coffee\_name | string           |
| Time\_of\_Day | category/string  |
| Weekday      | category/string  |
| Month\_name  | category/string  |
| Weekdaysort  | integer          |
| Monthsort    | integer          |
| Date         | date (YYYY-MM-DD)|
| Time         | time string      |

### Value Validation

**`hour_of_day`**
* Must be an integer in range 6–22 (dataset operating hours; no overnight transactions observed)

**`money`**
* Must be `>= 0`
* Observed range in dataset: 18.12–38.70
* Flag values outside this range as potential outliers for review

**`Weekdaysort`**
* Must be an integer in range 1–7

**`Monthsort`**
* Must be an integer in range 1–12

**`Time_of_Day`**
* Must be one of: `Morning`, `Afternoon`, `Night`
* Note: `Evening` does **not** exist in this dataset

**`cash_type`**
* Must be one of the known payment types present in the dataset
* Currently observed value: `card`
* Flag any unrecognised values for review

**`coffee_name`**
* Must be one of the 8 known products: `Americano`, `Americano with Milk`, `Cappuccino`, `Cocoa`, `Cortado`, `Espresso`, `Hot Chocolate`, `Latte`

**`Weekday`**
* Must be one of: `Mon`, `Tue`, `Wed`, `Thu`, `Fri`, `Sat`, `Sun` (3-letter abbreviation)

**`Month_name`**
* Must be one of: `Jan`, `Feb`, `Mar`, `Apr`, `May`, `Jun`, `Jul`, `Aug`, `Sep`, `Oct`, `Nov`, `Dec` (3-letter abbreviation)

**`Date`**
* Must be a valid ISO date in `YYYY-MM-DD` format

**`Time`**
* Must be a valid time string (format: `HH:MM:SS.ffffff`)

### Missing Data Rules

**Critical columns** — must not contain null values:

* `money`
* `coffee_name`
* `Date`
* `Time`

**Non-critical columns** — may be imputed or derived if missing:

* `Time_of_Day` — derivable from `hour_of_day`
* `Weekday` / `Weekdaysort` — derivable from `Date`
* `Month_name` / `Monthsort` — derivable from `Date`

---

## 8. Analytical Questions

Questions are grouped by complexity. All questions are verified to be answerable from the actual dataset contents.

> **Note on payment method questions:** The dataset contains only `card` transactions. Questions about comparing payment methods (e.g. cash vs card vs ewallet) are **not applicable** to this dataset. Analysis is limited to confirming `card` as the sole payment type.

### Core Questions (Primary)

1. What are the top-selling coffee products by transaction count?
2. What time of day (`Morning`, `Afternoon`, `Night`) generates the most revenue?
3. Which hour of the day has the highest sales activity?
4. Which weekday produces the highest total revenue?
5. Which coffee product generates the highest total revenue (not just volume)?

### Supporting Questions

6. Which coffee sells best during each time of day?
7. Which weekday has the lowest number of transactions?
8. How does total revenue change across months?
9. What is the average transaction value overall?
10. What is the average transaction value per coffee product?

### Advanced Questions

11. Are there strong time-of-day product preferences (which product dominates each time bucket)?
12. What is the full hourly sales distribution pattern across the operating day (6am–10pm)?
13. What weekday–hour combinations produce peak sales (heatmap analysis)?
14. Are there seasonal revenue trends across the 12-month period?
15. Which products are under-performing relative to the product mix average?

---

## 9. EDA Checkpoints

### Checkpoint 1 — Data Understanding

**Goal:** Establish a full picture of the raw dataset before any transformation.

Tasks:
* Print dataset shape (rows, columns)
* Show column data types (`dtypes`)
* Display sample rows (head, tail, random sample)
* List unique values per categorical column
* Confirm date range coverage

Questions answered:
* How many transactions exist? *(expected: 3,547)*
* How many distinct products are sold? *(expected: 8)*
* What hours are covered? *(expected: 6–22)*
* What is the date range? *(expected: 2024-03-01 → 2025-03-23)*

---

### Checkpoint 2 — Data Quality Assessment

**Goal:** Identify and document data quality issues before cleaning.

Tasks:
* Count missing values per column
* Detect and count duplicate rows
* Validate category values against allowed lists (products, time buckets, weekdays, months)
* Detect outliers in `money` column (IQR method or Z-score)
* Confirm `hour_of_day` values are within 6–22

Deliverables:
* Data quality report: counts of nulls, duplicates, invalid categories, outlier rows

---

### Checkpoint 3 — Temporal Exploration

**Goal:** Understand how sales and revenue are distributed over time.

Tasks:
* Transaction count per hour
* Revenue per hour
* Transaction count per weekday (ordered by `Weekdaysort`)
* Revenue per weekday
* Transaction count per month (ordered by `Monthsort`)
* Revenue per month
* Transaction count per `Time_of_Day` bucket

Visualizations:
* Bar chart: hourly transaction volume
* Bar chart: hourly revenue
* Bar chart: weekday revenue (Mon–Sun ordering)
* Line chart: monthly revenue trend
* Bar chart: revenue by time of day

---

### Checkpoint 4 — Product Analysis

**Goal:** Understand what sells and which products generate the most revenue.

Tasks:
* Transaction count per `coffee_name`
* Total revenue per `coffee_name`
* Average price per `coffee_name`
* Product sales count broken down by `Time_of_Day`
* Rank products by revenue and by volume separately

Visualizations:
* Horizontal bar chart: top products by transaction count
* Horizontal bar chart: top products by total revenue
* Grouped bar or stacked chart: product sales per time of day

---

### Checkpoint 5 — Behavioral Patterns

**Goal:** Uncover patterns in how products are purchased across time dimensions.

Tasks:
* Hour vs `coffee_name` transaction count heatmap
* Weekday vs `coffee_name` transaction count heatmap
* `Time_of_Day` vs `coffee_name` cross-tabulation
* Identify peak product per hour

Visualizations:
* Heatmap: hour × product
* Heatmap: weekday × product
* Summary table: dominant product per time bucket

> Payment method analysis is omitted as the dataset contains only `card` transactions — no meaningful comparison is possible.

---

## 10. Expected Insights

### Revenue Insights

* Identification of peak trading hours (likely morning and early afternoon based on coffee shop patterns)
* Identification of highest-revenue weekday(s) and lowest-revenue weekday(s)
* Monthly revenue trend showing seasonality or growth over the 12-month period

### Product Performance Insights

* Ranking of all 8 products by volume and by revenue
* Identification of highest and lowest revenue-generating products
* Time-specific product popularity — which product dominates Morning vs Afternoon vs Night

### Customer Behavior Insights

* Hourly buying patterns across the 6am–10pm operating window
* Weekday vs weekend comparison of sales volume and revenue
* Product preferences that shift across time-of-day segments

### Operational Insights

Actionable recommendations the analysis may support:

* **Staffing:** Schedule more staff during peak hours and peak weekday(s)
* **Promotions:** Target afternoon or low-revenue time slots with promotional offers
* **Inventory:** Prioritise stocking high-selling products; reduce waste on low-volume items
* **Product focus:** Push best-performing products during their peak time of day (e.g. promote Espresso in Morning if data confirms that pattern)

### Final Deliverables

1. Cleaned, validated dataset saved to `data/processed/`
2. EDA notebook (`notebooks/01_eda.ipynb`) with documented findings
3. Cleaning notebook (`notebooks/02_cleaning.ipynb`) with transformation log
4. Analysis notebook (`notebooks/03_analysis.ipynb`) with visualizations and insights
5. Summary report at `reports/summary.md`
6. Reproducible pipeline executable via `main.py`

---

## 11. Notebooks Writing Rules

All notebooks in `notebooks/` must follow these conventions.

### Structure

Each notebook must begin with a Markdown cell containing:
* Notebook title (H1)
* One-sentence description of the notebook's purpose
* Date last updated

Each major section must be separated by a Markdown cell with an H2 heading.

### Notebook Roles

| Notebook              | Purpose                                                         |
| --------------------- | --------------------------------------------------------------- |
| `01_eda.ipynb`        | Raw data exploration — shape, types, uniques, quick plots       |
| `02_cleaning.ipynb`   | Step-by-step data cleaning — document every transformation      |
| `03_analysis.ipynb`   | Final analysis — answer all Analytical Questions with charts    |

### Code in Notebooks

* Import all functions from `src/` — do not write raw analysis logic inline in notebooks
* Each code cell must do one thing (load data, run one analysis function, render one chart)
* No cell should exceed ~20 lines; extract longer logic into `src/`
* All chart cells must end with `plt.tight_layout()` and `plt.show()` (or equivalent for plotly)

### Output Requirements

* All notebooks must be fully executed (all cells run, outputs visible) before committing
* Charts must have titles, labelled axes, and legends where applicable
* No raw tracebacks or error outputs should remain in committed notebooks

### Data Access

* Notebooks load raw data via `src/ingestion/load_data.py` and via kaggle server directly `../kaggle/input/account-name/dataset-name/`
* Notebooks save processed data via `src/pipeline/run_pipeline.py` or direct calls to cleaning functions
* Notebooks must never write directly to `data/raw/` — raw data is immutable

### Additional Noteboook Rules
* Notebooks must be Kaggle-ready and Kaggle-friendly
* Notebooks must not contain any hardcoded file paths — use `src/config.py` for all path references
* Notebooks must be self-contained in terms of imports and data access — they should run without modification on any machine with the project dependencies installed
* Notebooks must include Markdown explanations of each step, especially in the analysis notebook where insights are drawn from the charts.
* Add Summary Section at the end of the notebook with key takeaways and insights derived from the analysis. 
