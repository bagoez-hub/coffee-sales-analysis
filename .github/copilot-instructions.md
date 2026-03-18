# Coffee Sales Dataset — Analysis Planning

## Data Analysis Overview

This project analyzes a transactional coffee shop sales dataset containing hourly purchase records, product names, payment types, and calendar time information. The goal of the analysis is to understand sales patterns, customer behavior, product performance, and time-based trends.

The dataset represents individual transactions and allows analysis across multiple time dimensions such as hour, weekday, and month. This makes the dataset suitable for time-series analysis, categorical analysis, and revenue aggregation.

The analysis will follow a structured data engineering style workflow including validation, cleaning, feature engineering, exploratory data analysis (EDA), and insight generation.

Primary objectives of the analysis:

* Understand when sales happen
* Understand what products sell the most
* Understand how customers pay
* Understand daily, weekly, and monthly patterns
* Generate business insights from transaction data

The final result should produce reproducible analysis, clear visualizations, and actionable insights that could be used for business decision making.

---

## 1. Dataset Column Meanings

| Column      | Meaning                                   | Example                               | Notes                                   |
| ----------- | ----------------------------------------- | ------------------------------------- | --------------------------------------- |
| hour_of_day | Hour when the transaction occurred (0–23) | 8                                     | Enables hourly sales analysis           |
| cash_type   | Payment method used for the purchase      | cash / card / ewallet                 | Useful for payment behavior analysis    |
| money       | Transaction value                         | 4.5                                   | Represents revenue from the sale        |
| coffee_name | Product purchased                         | Latte                                 | Enables product-level sales analysis    |
| Time_of_Day | Categorized time bucket                   | Morning / Afternoon / Evening / Night | Derived feature for behavioral patterns |
| Weekday     | Name of day                               | Monday                                | Used to analyze weekly patterns         |
| Month_name  | Month of transaction                      | January                               | Used for seasonality insights           |
| Weekdaysort | Numeric weekday order                     | 1–7                                   | Used for correct chronological sorting  |
| Monthsort   | Numeric month order                       | 1–12                                  | Prevents alphabetical sorting issues    |
| Date        | Calendar date of transaction              | 2023-05-14                            | Enables daily aggregation               |
| Time        | Exact transaction time                    | 08:34:12                              | Can be used to reconstruct timestamp    |

---

# 2. Validation Rules

Data validation ensures the dataset is reliable before analysis.

## Structural Validation

* Dataset must contain all required columns
* No duplicate column names

Required columns:

hour_of_day
cash_type
money
coffee_name
Time_of_Day
Weekday
Month_name
Weekdaysort
Monthsort
Date
Time

---

## Type Validation

| Column      | Expected Type   |
| ----------- | --------------- |
| hour_of_day | integer         |
| cash_type   | category/string |
| money       | float           |
| coffee_name | string          |
| Time_of_Day | category        |
| Weekday     | category        |
| Month_name  | category        |
| Weekdaysort | integer         |
| Monthsort   | integer         |
| Date        | date            |
| Time        | time            |

---

## Value Validation

hour_of_day

* must be between 0 and 23

money

* must be >= 0
* extreme outliers flagged

Weekdaysort

* range 1–7

Monthsort

* range 1–12

Time_of_Day

* must be one of:

  * Morning
  * Afternoon
  * Evening
  * Night

cash_type

* must belong to allowed categories

Date

* valid ISO date

Time

* valid time format

---

## Missing Data Rules

Critical columns must not contain null values:

* money
* coffee_name
* Date
* Time

Non‑critical columns can be imputed or derived.

---

# 3. Expected Analysis Questions

## Core Insights (Primary Questions)

1. What are the top selling coffee products?
2. What time of day generates the most revenue?
3. What hour has the highest sales activity?
4. Which weekday produces the highest revenue?
5. Which payment method is used the most?

---

## Supporting Insights

6. What coffee sells best during each time of day?
7. Which weekday has the lowest sales?
8. How does revenue change across months?
9. What is the average transaction value?
10. Which coffee generates the most revenue (not just quantity)?

---

## Advanced Insights

11. Are there strong time-of-day product preferences?
12. What is the hourly sales distribution pattern?
13. Does payment method vary by time of day?
14. What weekday-hour combinations produce peak sales?
15. Are there seasonal trends across months?

---

# 4. EDA Checkpoints (Milestones)

## Checkpoint 1 — Data Understanding

* Dataset shape
* Column data types
* Sample rows
* Unique values per column

Questions answered:

* How many transactions exist?
* How many products are sold?

---

## Checkpoint 2 — Data Quality Assessment

* Missing values
* Duplicate rows
* Invalid categories
* Outlier detection in money

Deliverables:

* Data quality report

---

## Checkpoint 3 — Temporal Exploration

* Transactions per hour
* Revenue per hour
* Revenue per weekday
* Revenue per month

Visualizations:

* Hourly sales distribution
* Weekday sales chart
* Monthly trend

---

## Checkpoint 4 — Product Analysis

* Sales count per coffee
* Revenue per coffee
* Product popularity by time of day

Visualizations:

* Top selling products
* Revenue by product

---

## Checkpoint 5 — Behavioral Patterns

* Payment method distribution
* Payment method by time of day
* Hour vs product heatmap

Visualizations:

* Heatmaps
* Time-product patterns

---

# 5. Expected Results and Insights

The analysis is expected to produce business insights such as:

## Revenue Insights

* Peak sales hours
* Peak revenue weekdays
* Monthly sales trend

## Customer Behavior Insights

* Preferred payment methods
* Buying patterns across the day
* Coffee preferences by time of day

## Product Performance

* Best selling coffee
* Highest revenue generating coffee
* Time-specific product popularity

## Operational Insights

Possible recommendations:

* Optimal staffing hours
* Best time for promotions
* Product focus during specific time periods

Example:

* Promote espresso during morning rush
* Offer afternoon discounts on slower products

---

# Final Outcome

The final deliverables of the project should include:

1. Clean validated dataset
2. Exploratory analysis notebook
3. Visualized insights
4. Summary report of key findings
5. Reproducible analysis pipeline

The insights generated should be actionable and provide value for business decision making. The analysis should be transparent, well-documented, and reproducible for future updates or similar datasets. 

# Dependencies
The analysis will require the following Python libraries:
* pandas
* matplotlib
* seaborn
* plotly (for interactive visualizations)
* numpy
* scikit-learn (for outlier detection)
* datetime
* Jupyter Notebook for analysis documentation
* python-dateutil (for date parsing)
* pydantic (for data validation)
* pytest (for testing validation rules)
* ipykernels (for Jupyter environment)
* loguru (for logging during data processing)
* pytest-cov (for test coverage reporting)
* black (for code formatting)
* ruff (for linting)

# Folder Structure
coffee-sales-analysis/
│
├── pyproject.toml
├── README.md
├── .gitignore
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── external/
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_cleaning.ipynb
│   └── 03_analysis.ipynb
│
├── src/
│   ├── config.py
│   │
│   ├── ingestion/
│   │   └── load_data.py
│   │
│   ├── validation/
│   │   └── schema.py
│   │
│   ├── cleaning/
│   │   └── clean_data.py
│   │
│   ├── features/
│   │   └── time_features.py
│   │
│   ├── analysis/
│   │   ├── sales_analysis.py
│   │   ├── time_analysis.py
│   │   └── product_analysis.py
│   │
│   ├── visualization/
│   │   └── plots.py
│   │
│   └── pipeline/
│       └── run_pipeline.py
│
├── tests/
│   ├── test_schema.py
│   ├── test_cleaning.py
│   └── test_features.py
│
└── reports/
    ├── figures/
    └── summary.md