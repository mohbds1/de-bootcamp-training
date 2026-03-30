# ☕ Cafe Sales Data Analysis

## Overview

A data cleaning and exploratory analysis pipeline for a dirty cafe sales dataset containing **10,000 transactions** from 2023. The project demonstrates robust data wrangling techniques—including time-aware imputation, identity reconciliation (`Quantity × Price = Total`), and hemisphere-configurable seasonality—followed by business-oriented exploratory analysis.

## Methodology

### 1. Data Cleaning Pipeline
| Step | Description |
|------|-------------|
| **Placeholder Removal** | Replaced sentinel values (`ERROR`, `UNKNOWN`) with `NaN` for proper missing-data handling |
| **Strict Date Parsing** | Multi-format parsing (`%Y-%m-%d`, `%d/%m/%Y`) with explicit fallback logic |
| **Time-Aware Price Imputation** | Missing prices filled using `Item + YearMonth` mode, with `Item + Month` seasonal fallback |
| **Item Recovery** | Missing items inferred from unambiguous price-to-item mappings |
| **Identity Reconciliation** | After rounding `Quantity` to integers, `Total_Spent` is recomputed to enforce `Qty × Price = Total` |
| **Imputation Provenance** | Boolean flag columns (`*_orig`) track which values are original vs. imputed, preventing compounding imputations |

### 2. Feature Engineering
- **Season** — Configurable by hemisphere (North/South/None)
- **YearMonth / Month / Year** — Temporal grouping keys for trend and seasonality analysis

### 3. Exploratory Data Analysis
- Top items by transaction frequency and by revenue
- Seasonal sales distribution
- Payment method market share
- Monthly revenue trend

## Key Findings

- **9,514 rows** retained after cleaning (95.1% retention rate from 10,000 raw records)
- **Coffee** and **Salad** are the most frequently sold items, while **Salad**, **Sandwich**, and **Smoothie** lead in revenue
- Sales are roughly **evenly distributed** across seasons
- **Digital Wallet**, **Credit Card**, and **Cash** share almost equal usage (~23% each total, or ~33% of known methods)
- ~32% of `Payment_Method` and ~40% of `Location` values were missing and labeled `Unknown`

## Project Structure

```
cafe-sales-data-analysis/
├── README.md
├── requirements.txt
├── data/
│   └── dirty_cafe_sales.csv      # Raw input (10,000 rows)
├── output/
│   └── cleaned_cafe_sales.csv    # Cleaned output (9,514 rows)
└── main.ipynb                    # Full pipeline: cleaning + EDA
```

## Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.x | Core language |
| Pandas | ≥ 1.5 | Data manipulation |
| NumPy | ≥ 1.23 | Numerical operations |
| Matplotlib | ≥ 3.6 | Static visualizations |
| Seaborn | ≥ 0.12 | Statistical plots |

## Getting Started

### Prerequisites
- Python 3.9+ recommended
- pip or conda

## How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Execution

Follow these steps to run the data cleaning pipeline:

#### 1. Prepare the dataset
Place the raw dataset in the following path:
```

data/dirty_cafe_sales.csv

```

#### 2. Open the notebook
Open the notebook using Jupyter:
```

main.ipynb

```

#### 3. Run the pipeline
From the menu:
```

Kernel → Restart & Run All

```

---

### ⚙️ What the pipeline does

Once executed, the pipeline will:

1. Load the raw dataset from:
   `data/dirty_cafe_sales.csv`

2. Perform:
   - Data cleaning  
   - Data validation  
   - Data transformation  

3. Save cleaned outputs to:
   `Output/`

4. Generate:
   - EDA (Exploratory Data Analysis) visualizations  
   - Display results inline inside the notebook  

---

### 📁 Output

After execution, you will find:
- Cleaned dataset(s) inside `Output/`
- Visual insights directly in the notebook

## Data Dictionary

### Input (`dirty_cafe_sales.csv`)

| Column | Type | Description |
|--------|------|-------------|
| `Transaction ID` | string | Unique transaction identifier (e.g., `TXN_1961373`) |
| `Item` | string | Product name (Coffee, Cake, Cookie, Salad, Sandwich, Smoothie, Juice, Tea, etc.) |
| `Quantity` | string* | Number of units purchased |
| `Price Per Unit` | string* | Unit price in local currency |
| `Total Spent` | string* | Transaction total |
| `Payment Method` | string | Cash, Credit Card, Digital Wallet, Debit Card, or missing |
| `Location` | string | In-store, Takeaway, or missing |
| `Transaction Date` | string | Date in `YYYY-MM-DD` or `DD/MM/YYYY` format |

\* *Stored as `object` dtype due to embedded `ERROR` / `UNKNOWN` placeholders.*

### Output (`cleaned_cafe_sales.csv`)

| Column | Type | Description |
|--------|------|-------------|
| `Transaction_ID` | string | Cleaned identifier |
| `Item` | string | Product name (`Unknown` for unrecoverable items) |
| `Quantity` | Int64 | Integer quantity |
| `Price_Per_Unit` | float64 | Numeric unit price |
| `Total_Spent` | float64 | Reconciled total (`Quantity × Price_Per_Unit`) |
| `Payment_Method` | string | Payment type (`Unknown` for missing) |
| `Location` | string | Transaction location (`Unknown` for missing) |
| `Transaction_Date` | datetime64 | Parsed date |
| `Year` | float64 | Extracted year |
| `YearMonth` | period[M] | Year-month period for grouping |
| `Month` | float64 | Extracted month number |
| `Season` | string | Derived season (hemisphere-configurable) |