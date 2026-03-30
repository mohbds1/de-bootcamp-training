# Nike Sales Data Cleaning Pipeline

A comprehensive, data cleaning pipeline for a raw Nike sales dataset containing **2,500 records** across **13 columns**. The project transforms unclean, inconsistent, and incomplete data into a structured, reliable, and analysis-ready dataset.

> **Note:** This project focuses exclusively on data cleaning and validation. It does not include exploratory analysis or modeling.

---

## Table of Contents

- [Dataset Description](#dataset-description)
- [Why This Pipeline Exists](#why-this-pipeline-exists)
- [Project Structure](#project-structure)
- [Methodology](#methodology)
- [Assumptions & Limitations](#assumptions--limitations)
- [Output Data Schema](#output-data-schema)
- [How to Run](#how-to-run)
- [Results Summary](#results-summary)
- [Technologies Used](#technologies-used)

---

## Dataset Description

**Source:** [Kaggle — Nike Sales (Uncleaned)](https://www.kaggle.com/datasets/nayakganesh007/nike-sales-uncleaned-dataset)
**File:** `data/Nike_Sales_Uncleaned.csv`

| Column | Description |
|--------|-------------|
| `Order_ID` | Unique identifier for each order |
| `Gender_Category` | Customer segment — Men, Women, Kids |
| `Product_Line` | Product category — Running, Soccer, Training, Lifestyle, Basketball |
| `Product_Name` | Specific product name |
| `Size` | Product size (mixed apparel + shoe sizing) |
| `Units_Sold` | Number of units sold (negative = return) |
| `MRP` | Maximum Retail Price per unit |
| `Discount_Applied` | Discount percentage (0.0 – 1.0 range) |
| `Revenue` | Total revenue for the order |
| `Order_Date` | Date of order (mixed formats) |
| `Sales_Channel` | Online or Retail |
| `Region` | Geographic region in India |
| `Profit` | Profit for the order |

### Key Data Quality Issues Identified

The raw dataset downloaded from Kaggle contained **severe and widespread data quality issues** that made it unusable for any analysis in its original state:

| Issue | Severity | Count |
|-------|----------|-------|
| Missing `Discount_Applied` | High | 1,668 (66.7%) |
| Missing `MRP` | High | 1,254 (50.2%) |
| Missing `Units_Sold` | High | 1,235 (49.4%) |
| Unparsed `Order_Date` | Medium | 616 (24.6%) |
| Missing `Size` | Medium | 510 (20.4%) |
| Invalid discounts (> 100%) | Medium | 180 |
| Negative `Units_Sold` (returns) | Low | 205 |
| Fragmented `Region` names | Low | 9 → 6 unique |

> **In total, over 50% of the core numerical fields were missing.** This is not a typical cleaning task — it required designing a multi-stage imputation strategy to recover as much meaning as possible from the available data.

---

## Why This Pipeline Exists

The raw Kaggle dataset presents a real-world challenge: **the majority of critical fields (Units_Sold, MRP, Discount) are missing**, with Revenue often recorded as zero. This makes the data completely unusable without intervention.

Rather than discarding half the dataset, this pipeline takes a **transparent, non-destructive approach**:

1. **No rows are deleted** — every record is preserved, even returns and incomplete entries
2. **Every imputation is flagged** — boolean flags track exactly which values were original vs. imputed
3. **Two output files** — a clean version for analysis and a full audit version for traceability
4. **Business logic validation** — automated checks ensure internal consistency after cleaning

This project demonstrates how to handle severely degraded data while maintaining full transparency for downstream consumers.

---

## Project Structure

```
nike-sales-data-cleaning/
├── data/
│   └── Nike_Sales_Uncleaned.csv          # Raw input dataset (from Kaggle)
├── Output/
│   ├── Nike_Sales_Cleaned_Final.csv      # Compact cleaned dataset (22 columns)
│   └── Nike_Sales_Audit_Full.csv         # Full audit dataset with raw snapshots & flags (38 columns)
├── main.ipynb                            # Complete cleaning pipeline notebook
├── README.md                             # Project documentation
├── requirements.txt                      # Python dependencies
```

---

## Methodology

The pipeline follows a strict **Audit → Clean → Validate → Export** workflow with non-destructive transformations. A raw snapshot (`df_raw`) is preserved throughout for auditability.

### Step 1: Initial Data Inspection
- Structural assessment: shape, dtypes, sample rows
- Missing value profiling across all columns
- Duplicate detection (0 exact duplicates found)

### Step 2: Data Quality Diagnostics
- Comprehensive missing value analysis with percentages
- Invalid value detection (discounts > 100%, negative units, zero revenue)
- Region fragmentation mapping (e.g., "bengaluru" vs "Bangalore", "hydrabad" vs "Hyderabad")
- Date format inconsistency cataloging (ISO, DD-MM-YYYY, YYYY/MM/DD)

### Step 3: Structural Cleaning (Zero Row Deletions)
| Action | Details |
|--------|---------|
| **Return Flagging** | Created `is_return` boolean flag for negative `Units_Sold` (205 rows) |
| **Discount Repair** | Offset correction for values in [1.0, 1.3] range (subtract 1.0); remaining invalids → NaN |
| **Date Standardization** | Multi-stage parsing: ISO → DD-MM-YYYY → fallback. Original preserved in `Order_Date_raw` |
| **Region Normalization** | Unified 9 variants → 6 standard names (497 rows corrected) |
| **Size Normalization** | Stripped whitespace, kept as categorical text (mixed apparel + shoe sizes) |

### Step 4: Advanced Imputation
A hybrid strategy: **deterministic recovery → group-based statistical imputation → conservative fallbacks**.

| Column | Strategy | Result |
|--------|----------|--------|
| **MRP** | Product_Name median → Product_Line median → global median | 1,254 → 0 missing |
| **Units_Sold** | Phase A: Revenue-based recovery (baseline=1 if Revenue > 0). Phase B: **Group median** from positive sales (Product_Name → Product_Line → global), rounded to whole numbers | 1,235 → 0 missing |
| **Discount_Applied** | Product_Name → Product_Line → Sales_Channel → global median, then clamped [0, 1] | 1,668 → 0 missing |
| **Size** | Product_Name mode → (Gender_Category, Product_Line) mode → global mode | 510 → 0 missing |
| **Order_Date** | Intentionally left as NaT where parsing failed — flagged via `Date_Missing_Flag` | 616 remain |

> **Why group-median for Units_Sold?** The raw dataset had Revenue = 0 for nearly all rows with missing Units_Sold, making formula-based recovery (`Units_Sold = Revenue / MRP`) impossible. Group-median imputation uses the typical sales volume for each product — the same proven methodology applied to MRP and Discount — ensuring downstream Revenue calculations produce meaningful values rather than zeros.

### Step 5: Revenue Reconciliation
- Calculated `Revenue_calc = Units_Sold × MRP × (1 - Discount_Applied)`
- Created `Revenue_final` using rule: prefer raw revenue if valid, otherwise use calculated
- Flagged rows where calculated revenue was used (`Revenue_Used_Calc_Flag`)
- Negative raw revenue values (returns) are always preserved

### Step 6: Outlier Handling (Winsorization)
| Metric | Method | Cap | Rows Affected |
|--------|--------|-----|---------------|
| **Revenue** | IQR upper bound on positive values only | 25,572.46 | 9 rows capped |
| **Profit** | Percentile [0.5%, 99.5%] two-sided | [-1,181.55, 3,967.71] | 26 rows capped |

Additional flags: `Revenue_Outlier_Flag`, `Profit_Outlier_Flag`, `Profit_Ratio_Flag` (profit > 2× revenue).

### Step 7: Final Validation
- **Structural checks:** All core fields (except `Order_Date`) confirmed 100% complete
- **Range checks:** Discount values within [0, 1], MRP > 0
- **Integrity checks:** No duplicate rows, 2,500 rows preserved
- **Business logic checks:** Return flag consistency, Zero-sales flag consistency, Revenue calculation accuracy (max diff = 0.0000), Imputation flag count matches raw NaN count

---

## Assumptions & Limitations

> **Important:** The raw dataset from Kaggle had extreme levels of missing data. The following assumptions were made to produce a usable output:

1. **49.4% of Units_Sold were imputed via group median (1,235 rows):** The original values were missing (NaN). Since Revenue was also 0 for these rows, formula-based recovery was impossible. Group-median imputation was chosen to produce realistic values. All imputed rows are flagged via `Units_Sold_Imputed_Flag`.

2. **9.0% of records remain as zero-sales (224 rows):** These are rows where `Units_Sold` was genuinely 0 in the raw data (not imputed). Flagged via `Is_Zero_Sales`.

3. **93.5% of Revenue_final uses calculated values:** Due to the prevalence of zero raw revenue, most `Revenue_final` values are derived from `Units_Sold × MRP × (1 - Discount)`. This is now meaningful because Units_Sold uses realistic imputed values.

4. **24.6% of Order_Date values are missing:** Dates were intentionally left as NaT where reliable parsing was not possible. Time-series analyses should account for this gap via `Date_Missing_Flag`.

5. **MRP imputation uses group medians:** 50.2% of MRP values were imputed using Product_Name or Product_Line medians. Flagged via `MRP_Imputed_Flag`.

6. **Discount imputation uses multi-level fallback:** 66.7% of discounts were imputed with up to 4 levels of fallback (product → line → channel → global). Some values may not accurately reflect the specific product.

7. **Return transactions preserved:** 205 negative `Units_Sold` records are retained and flagged (`is_return = True`), not deleted.

---

## Output Data Schema

### Cleaned Final (`Nike_Sales_Cleaned_Final.csv`) — 22 columns

| Column | Type | Description |
|--------|------|-------------|
| `Order_ID` | int | Unique order identifier |
| `Gender_Category` | str | Men / Women / Kids |
| `Product_Line` | str | Product category |
| `Product_Name` | str | Specific product |
| `Size` | str | Product size |
| `Units_Sold` | int64 | Units sold (imputed via group median where missing; negative = return) |
| `MRP` | float | Maximum Retail Price (imputed where missing) |
| `Discount_Applied` | float | Discount rate [0.0, 1.0] |
| `Revenue` | float | Final reconciled revenue |
| `Revenue_Capped` | float | Revenue after Winsorization |
| `Order_Date` | datetime | Parsed order date (NaT if unparsable) |
| `Sales_Channel` | str | Online / Retail |
| `Region` | str | Normalized region name |
| `Profit` | float | Profit value |
| `Profit_Capped` | float | Profit after Winsorization |
| `is_return` | bool | True if Units_Sold < 0 |
| `Is_Zero_Sales` | bool | True if Units_Sold = 0 and MRP > 0 |
| `Units_Sold_Imputed_Flag` | bool | True if Units_Sold was originally missing and imputed via group median |
| `Date_Missing_Flag` | bool | True if Order_Date could not be parsed |
| `Revenue_Outlier_Flag` | bool | True if revenue was capped |
| `Profit_Outlier_Flag` | bool | True if profit was capped |
| `Profit_Ratio_Flag` | bool | True if |Profit| > 2× |Revenue| |

### Audit Full (`Nike_Sales_Audit_Full.csv`) — 38 columns
Contains all columns above plus raw snapshots (`Units_Sold_raw`, `MRP_raw`, `Discount_Applied_raw`, `Revenue_raw`, `Profit_raw`, `Order_Date_raw`) and detailed imputation flags for full traceability.

---

## How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Execution
1. Place the raw dataset at `data/Nike_Sales_Uncleaned.csv`
2. Open `main.ipynb` in Jupyter Notebook or JupyterLab
3. Run all cells sequentially (Kernel → Restart & Run All)
4. Cleaned outputs will be saved to the `Output/` directory

---

## Results Summary

| Metric | Before | After |
|--------|--------|-------|
| Total Rows | 2,500 | 2,500 (preserved) |
| Missing Core Fields | Multiple columns with 20-67% missing | 0 missing (except Order_Date: 616) |
| Zero-Sales Rows | — | 224 (9.0%) — genuine zeros only |
| Unique Regions | 9 (fragmented) | 6 (normalized) |
| Invalid Discounts | 180 (> 100%) | 0 |
| Duplicate Rows | 0 | 0 |
| Outliers Capped (Revenue) | — | 9 rows |
| Outliers Capped (Profit) | — | 26 rows |
| Imputation Flags | — | 11 transparent flags |
| Business Logic Checks | — | 4/4 passed |

---

## Technologies Used

- **Python 3.10+**
- **pandas** — Data manipulation and cleaning
- **NumPy** — Numerical operations
- **Matplotlib** — Distribution visualization and QA charts
- **missingno** — Missing data visualization (before/after comparison)
