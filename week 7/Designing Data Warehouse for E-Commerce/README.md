# Designing Data Warehouse for E-Commerce

Small end-to-end example: **SQLite (OLTP-style source) → Python ETL → PostgreSQL star schema**, built around the Olist e-commerce dataset pattern. The goal is a warehouse you can query for sales, customers, categories, and delivery behaviour without repeating the messy joins from the source every time.

## What this repo does

Source tables land in **Bronze** as-is. **Silver** cleans and integrates them (deduped customers, joined orders/items/products/payments, delivery metrics). **Gold** follows a simple star schema approach: dimensions for date, customer, product, and seller, plus facts at **order-item** grain (`fact_sales`) and **order** grain (`fact_delivery`).

The pipeline is scripted in `data_pipeline.py` (extract, bronze load, silver transform, gold load). Design detail lives in `Data Warehouse Design and Implementation Report.md`.

## Design choices worth calling out

**Payments.** One order can have more than one payment row. Merging payments directly onto order items would duplicate lines and inflate revenue. Therefore, payments are aggregated **per `order_id`** (taking the maximum installments and one `payment_type`) before joining — **without carrying the total `payment_value`**. This avoids any risk of double-counting a monetary value at the order-item grain. Revenue analysis relies on `price + freight_value` per line, which is always at the correct grain.

**Revenue in reporting.** Item revenue is taken as **`price + freight_value`** per line, consistent with the `total_item_value` field produced in Silver. That matches how the example SQL reports “total revenue” and customer lifetime value.

**Delivery analysis.** `fact_delivery` is one row per order. Reporting differentiates two views:

- **Seller-based delivery performance** — links delivery to seller geography via `fact_sales`, but only at **`(order_id, seller_key)`** so multiple items from the same seller do not duplicate the same delivery.
- **Customer-based delivery experience** — joins `fact_delivery` to `dim_customers` on `customer_key` for a customer-state view without touching line items.

**Date dimension.** `dim_date` is generated as a full calendar range — from the earliest purchase date to the latest actual delivery date — using a `generate_series` in the Gold load. This guarantees that all date keys used in both `fact_sales` and `fact_delivery` (including estimated and actual delivery dates) resolve correctly in any join. The dimension includes calendar attributes (day name, month, quarter, **weekday vs weekend**) to enable time-of-week analysis and any time-based drill-downs.

*Why `payment_value` was removed from `fact_sales`:* The fact grain is the order item. An order-level monetary total would repeat on every line for that order and break aggregations. Keeping payment behaviour as attributes (`payment_type`, `payment_installments`) is safe; revenue is computed from item `price` and `freight_value` only.

## Repository layout

| File | Role |
|------|------|
| `data_pipeline.py` | Orchestrates extract, bronze/silver/gold loads; logging and retry wrapper around extract. |
| `etl_logic.py` | Sales transform (per-order payment attributes: max installments, one `payment_type`; category fill; date key; `total_item_value`) and delivery KPIs plus delivery date keys. |
| `dw_ddl.sql` | PostgreSQL DDL: dimensions, facts, indexes; `fact_sales` partitioned by `order_purchase_date_key`. |
| `reporting_queries.sql` | Example analytics: trends, top customers, category revenue; **two separate delivery analyses** — seller-based (via `fact_sales` at `(order_id, seller_key)`) vs customer-based (via `fact_delivery` and `dim_customers`) — so duplication across facts is avoided. |
| `Data Warehouse Design and Implementation Report.md` | Written design rationale (architecture, model, reporting). |

`fact_leads` is included in the DDL for future extension, but is not loaded in the current pipeline.

## Prerequisites

- Python 3.9+
- PostgreSQL (empty database, user with rights to create objects)
- **`olist.sqlite`** in the project directory (or adjust `source_db_path` in code). The file is **not** in the repo (ignored in `.gitignore` because it is large); obtain the Olist dataset and build or download a SQLite copy as needed.

Install packages:

```bash
pip install pandas sqlalchemy psycopg2-binary numpy
```

## Run

1. Create a database and run **`dw_ddl.sql`** against it (creates tables, partitions, indexes).

2. Set the warehouse connection: either pass `target_db_url` when constructing `ECommercePipeline`, or set the environment variable **`DATABASE_URL`** (for example `postgresql://user:password@localhost:5432/ecommerce_dw`). The default in code uses a placeholder password — replace it or use `DATABASE_URL` before running.

3. Execute:

```bash
python data_pipeline.py
```

Logs go to **`pipeline.log`** and the console.

Gold load is **truncate-and-reload** for the tables the script touches (`dim_*` and facts it fills), so each run replaces analytical data rather than appending incrementally.

## Reporting

Open **`reporting_queries.sql`** in your SQL client against the warehouse. Queries are numbered and commented; delivery section labels **seller-based** vs **customer-based** explicitly so the two questions do not get mixed up.
All queries are designed to avoid double counting when joining across fact tables.

---

During development, the main challenge was avoiding duplication when combining payments and order items.

If you extend the project (e.g. load `fact_leads`, incremental loads, or more dimensions), keep the same grain rules: match fact grain to the business process, and avoid many-to-one joins that duplicate facts when you aggregate.
