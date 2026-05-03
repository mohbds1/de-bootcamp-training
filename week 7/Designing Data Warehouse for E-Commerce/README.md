# Designing a Data Warehouse for E-Commerce

Week 7 bootcamp project: an end-to-end **medallion-style pipeline** that moves Brazilian e-commerce data (**Olist-style SQLite OLTP** → **Python ETL** → **PostgreSQL star schema**). The warehouse answers questions about revenue, customer value, product categories, and delivery performance without repeating fragile many-to-many joins at query time.

## What the system does

1. **Extract** seven normalized tables from a local SQLite file (`olist.sqlite`).
2. **Load (Bronze)** each table into PostgreSQL as `bronze_<table_name>` with an `ingested_at` timestamp (full replace per run).
3. **Transform (Silver)** in pandas: deduplicated customers, integrated sales lines with per-order payment attributes, English category labels, integer date keys, and order-level delivery KPIs.
4. **Load (Gold)** with SQL inside a single transaction: truncate dimensions and facts (with cascade), rebuild `dim_date` from a calendar `generate_series`, insert dimensions from Bronze/Silver, then load `fact_sales` and `fact_delivery`.

Each full run is **truncate-and-reload** for the Gold objects the script manages, so analytical tables are rebuilt from the latest source snapshot rather than incrementally merged.

```mermaid
flowchart LR
  subgraph source [Source]
    SQLite[(olist.sqlite)]
  end
  subgraph bronze [Bronze in PostgreSQL]
    B1[bronze_orders ... bronze_order_payments]
  end
  subgraph silver [Silver in PostgreSQL]
    S1[silver_customers]
    S2[silver_sales]
    S3[silver_delivery]
  end
  subgraph gold [Gold star schema]
    D[dim_date dim_customers dim_products dim_sellers]
    F[fact_sales fact_delivery]
  end
  SQLite -->|pandas read_sql| B1
  B1 -->|pandas transforms| S1 & S2 & S3
  S1 & S2 & S3 & B1 -->|SQL INSERT| D & F
```

## Source → Bronze mapping

| SQLite table | Bronze table |
|--------------|--------------|
| `orders` | `bronze_orders` |
| `order_items` | `bronze_order_items` |
| `customers` | `bronze_customers` |
| `products` | `bronze_products` |
| `sellers` | `bronze_sellers` |
| `product_category_name_translation` | `bronze_product_category_name_translation` |
| `order_payments` | `bronze_order_payments` |

## Silver layer (logic in `etl_logic.py`)

- **`silver_customers`**: `bronze_customers` with duplicates removed on `customer_id`.
- **`silver_sales`**: `transform_data` merges order lines with orders, **aggregates payments per `order_id`** (max `payment_installments`, first `payment_type`), joins products and category translation, fills missing English category with `unknown`, builds `order_purchase_date_key` (`YYYYMMDD` int), and adds `total_item_value = price + freight_value`.
- **`silver_delivery`**: `calculate_delivery_performance` on `orders` computes `days_to_delivery`, `is_late` (actual vs estimated), and purchase / estimated / actual **date keys** aligned with `dim_date`.

## Gold layer (star schema)

| Object | Grain | Notes |
|--------|--------|--------|
| `dim_date` | Calendar day | Built from min purchase date in `silver_sales` through max actual delivery in `silver_delivery`; includes weekday/weekend and calendar attributes. |
| `dim_customers` | Customer | From `silver_customers`. |
| `dim_products` | Product | From `bronze_products` left join translation table for English category name. |
| `dim_sellers` | Seller | From `bronze_sellers`. |
| `fact_sales` | **Order line item** | Measures: `price`, `freight_value`, `payment_installments`, `payment_type`. Partitioned by `order_purchase_date_key` (range); the pipeline ensures a **default** partition exists for loads. |
| `fact_delivery` | **Order** | One row per `order_id`: delivery timing keys, `days_to_delivery`, `is_late`. |
| `fact_leads` | Lead (optional) | Present in `dw_ddl.sql` for extension; **not** loaded by the current pipeline. |

The DDL defines `fact_delivery.delivery_status`, but the current ETL does not populate it; analytics in `reporting_queries.sql` use the timing and `is_late` fields.

## Design choices (grain and money)

**Payments.** One order can have multiple payment rows. Merging raw payments onto order items would duplicate lines and distort revenue. Payments are aggregated **per `order_id`** before the join. **`payment_value` is intentionally not carried** into `fact_sales` at line-item grain, so order-level totals cannot be double-counted when summing facts. Revenue in this model is **`price + freight_value` per line**, consistent with `total_item_value` in Silver and the example reports.

**Delivery reporting.** Two complementary views avoid double-counting:

- **Seller-based** — link `fact_delivery` to sellers via **`DISTINCT (order_id, seller_key)`** from `fact_sales` so multiple lines from the same seller do not duplicate the same delivery.
- **Customer-based** — join `fact_delivery` to `dim_customers` for state-level delivery experience without going through line items.

## Code map

| File | Role |
|------|------|
| `data_pipeline.py` | `ECommercePipeline`: SQLite extract (with retry), Bronze load, Silver orchestration, Gold SQL load; logging to console and `pipeline.log`. |
| `etl_logic.py` | `transform_data`, `calculate_delivery_performance` — all pandas Silver rules. |
| `dw_ddl.sql` | PostgreSQL DDL: dimensions, facts, indexes; `fact_sales` defined as a range-partitioned table. |
| `reporting_queries.sql` | Example analytics: revenue trends, top customers by lifetime value, category revenue, seller- vs customer-based delivery metrics. |

## Prerequisites

- **Python 3.9+**
- **PostgreSQL** (empty database; user can create tables)
- **`olist.sqlite`** in the same directory you run the script from (or pass a custom path to `ECommercePipeline`). The SQLite file is **not** committed (see `.gitignore`); use the [Olist Brazilian E-Commerce public dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) or equivalent export.

Install dependencies:

```bash
pip install pandas sqlalchemy psycopg2-binary numpy
```

## Configuration and run

1. Create a database and execute **`dw_ddl.sql`** once (creates dimensions, facts, indexes, partitioned `fact_sales`).

2. Set the warehouse URL:
   - Environment variable **`DATABASE_URL`** (recommended), e.g. `postgresql://user:password@localhost:5432/ecommerce_dw`, **or**
   - Pass `target_db_url` when constructing `ECommercePipeline`, **or**
   - Edit the placeholder in `_DEFAULT_TARGET_DB_URL` inside `data_pipeline.py` (not recommended for secrets).

3. From this project folder (so `olist.sqlite` and `pipeline.log` resolve as expected):

```bash
python data_pipeline.py
```

Optional programmatic use:

```python
from data_pipeline import ECommercePipeline

pipeline = ECommercePipeline(
    target_db_url="postgresql://user:pass@localhost:5432/ecommerce_dw",
    source_db_path="olist.sqlite",
)
pipeline.run_pipeline()
```

## Reporting

Run the numbered, commented statements in **`reporting_queries.sql`** in your SQL client against the warehouse. Delivery sections are explicitly labeled **seller-based** vs **customer-based** so aggregations stay at the correct grain.

## Extending the project

If you add incremental loads, more facts (e.g. populate `fact_leads`), or new dimensions, keep **fact grain** aligned to the business process and avoid many-to-one joins that duplicate fact rows when users sum measures.

---

*Part of a Data Engineering bootcamp portfolio (A1 Consulting).*
