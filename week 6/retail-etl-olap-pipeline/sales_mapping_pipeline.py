import os

import pandas as pd
from dotenv import load_dotenv
from hijri_converter import convert
from sqlalchemy import create_engine, text

load_dotenv()

# ---------------------------------------------------------
# 1. Database connections (URLs from environment — see .env.example)
# ---------------------------------------------------------

_oltp_url = os.getenv("RETAIL_OLTP_URL")
_olap_url = os.getenv("RETAIL_OLAP_URL")

if not _oltp_url or not _olap_url:
    raise SystemExit(
        "Missing RETAIL_OLTP_URL or RETAIL_OLAP_URL.\n"
        "Copy .env.example to .env, set both URLs, then run again."
    )

source_engine = create_engine(_oltp_url)
target_engine = create_engine(_olap_url)

# ---------------------------------------------------------
# 2. Make sure OLAP dim_date has the new Hijri columns
#    then clean OLAP tables before loading
# ---------------------------------------------------------

with target_engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE dim_date 
        ADD COLUMN IF NOT EXISTS is_ramadan BOOLEAN;

        ALTER TABLE dim_date 
        ADD COLUMN IF NOT EXISTS is_eid_al_fitr BOOLEAN;

        ALTER TABLE dim_date 
        ADD COLUMN IF NOT EXISTS is_eid_al_adha BOOLEAN;
    """))

    conn.execute(text("""
        TRUNCATE TABLE
            fact_order_sales,
            dim_date,
            dim_customer,
            dim_product,
            dim_store,
            dim_payment_type
        RESTART IDENTITY CASCADE;
    """))

print("OLAP schema checked and tables cleaned")

# ---------------------------------------------------------
# 3. Extract data from OLTP
# ---------------------------------------------------------

users = pd.read_sql("SELECT * FROM users", source_engine)
products = pd.read_sql("SELECT * FROM products", source_engine)
brands = pd.read_sql("SELECT * FROM brands", source_engine)
categories = pd.read_sql("SELECT * FROM categories", source_engine)
branches = pd.read_sql("SELECT * FROM branches", source_engine)
payment_methods = pd.read_sql("SELECT * FROM payment_methods", source_engine)
orders = pd.read_sql("SELECT * FROM orders", source_engine)
order_items = pd.read_sql("SELECT * FROM order_items", source_engine)
payments = pd.read_sql("SELECT * FROM payments", source_engine)

print("Step 1: Data extracted from OLTP database")

# ---------------------------------------------------------
# 4. Build dimensions
# ---------------------------------------------------------

dim_customer = users.rename(columns={
    "user_id": "customer_key",
    "full_name": "customer_name"
})[[
    "customer_key",
    "customer_name",
    "email",
    "address"
]].drop_duplicates()

dim_customer["city"] = dim_customer["address"]

dim_customer = dim_customer[[
    "customer_key",
    "customer_name",
    "email",
    "city"
]]

dim_product = products.merge(
    brands[["brand_id", "brand_name"]],
    on="brand_id",
    how="left"
).merge(
    categories[["category_id", "category_name"]],
    on="category_id",
    how="left"
)

dim_product = dim_product.rename(columns={
    "product_id": "product_key",
    "category_name": "category"
})[[
    "product_key",
    "product_name",
    "category"
]].drop_duplicates()

dim_store = branches.rename(columns={
    "branch_id": "store_key",
    "branch_name": "store_name",
    "city": "branch_city"
})[[
    "store_key",
    "store_name",
    "branch_city"
]].drop_duplicates()

dim_payment_type = payment_methods.rename(columns={
    "method_id": "payment_type_key",
    "method_name": "payment_type_name"
})[[
    "payment_type_key",
    "payment_type_name"
]].drop_duplicates()

print("Step 2: Dimensions created")

# ---------------------------------------------------------
# 5. Date handling
# ---------------------------------------------------------

orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["date_key"] = orders["order_date"].dt.strftime("%Y%m%d").astype(int)

dim_date = orders[[
    "date_key",
    "order_date"
]].drop_duplicates().rename(columns={
    "order_date": "full_date"
})

dim_date["day_number"] = dim_date["full_date"].dt.day
dim_date["month_number"] = dim_date["full_date"].dt.month
dim_date["month_name"] = dim_date["full_date"].dt.month_name()
dim_date["quarter_number"] = dim_date["full_date"].dt.quarter
dim_date["year_number"] = dim_date["full_date"].dt.year
dim_date["weekday_name"] = dim_date["full_date"].dt.day_name()
dim_date["is_weekend"] = dim_date["weekday_name"].isin(["Friday", "Saturday"])

# ---------------------------------------------------------
# 6. Hijri calendar handling
# Ramadan = Hijri month 9
# Eid Al-Fitr = first 3 days of Hijri month 10
# Eid Al-Adha = days 10 to 13 of Hijri month 12
# ---------------------------------------------------------

def get_hijri_date(gregorian_date):
    return convert.Gregorian(
        gregorian_date.year,
        gregorian_date.month,
        gregorian_date.day
    ).to_hijri()


dim_date["hijri_date"] = dim_date["full_date"].apply(get_hijri_date)

dim_date["is_ramadan"] = dim_date["hijri_date"].apply(
    lambda h: h.month == 9
)

dim_date["is_eid_al_fitr"] = dim_date["hijri_date"].apply(
    lambda h: h.month == 10 and h.day in [1, 2, 3]
)

dim_date["is_eid_al_adha"] = dim_date["hijri_date"].apply(
    lambda h: h.month == 12 and h.day in [10, 11, 12, 13]
)

dim_date = dim_date[[
    "date_key",
    "full_date",
    "day_number",
    "month_number",
    "month_name",
    "quarter_number",
    "year_number",
    "weekday_name",
    "is_weekend",
    "is_ramadan",
    "is_eid_al_fitr",
    "is_eid_al_adha"
]]

print("Step 3: Date dimension created with Hijri calendar flags")

# ---------------------------------------------------------
# 7. Build fact table
# ---------------------------------------------------------

payments_for_fact = payments[[
    "order_id",
    "method_id"
]].drop_duplicates(subset=["order_id"])

fact = order_items.merge(
    orders[[
        "order_id",
        "user_id",
        "branch_id",
        "date_key"
    ]],
    on="order_id",
    how="left"
).merge(
    payments_for_fact,
    on="order_id",
    how="left"
)

fact["sales_amount"] = fact["quantity"] * fact["unit_sale_price"]
fact["cost_amount"] = fact["quantity"] * fact["unit_purchase_price"]
fact["profit_amount"] = fact["sales_amount"] - fact["cost_amount"]

fact_order_sales = fact.rename(columns={
    "user_id": "customer_key",
    "product_id": "product_key",
    "branch_id": "store_key",
    "method_id": "payment_type_key"
})[[
    "date_key",
    "customer_key",
    "product_key",
    "store_key",
    "payment_type_key",
    "order_id",
    "quantity",
    "sales_amount",
    "cost_amount",
    "profit_amount"
]]

print("Step 4: Fact table created")

# ---------------------------------------------------------
# 8. Validation
# ---------------------------------------------------------

print("Order items count:", len(order_items))
print("Fact table count:", len(fact_order_sales))

if len(order_items) != len(fact_order_sales):
    raise Exception("Data validation failed: some order items were lost.")
else:
    print("Validation passed: no data loss detected")

# ---------------------------------------------------------
# 9. Load data into OLAP
# ---------------------------------------------------------

dim_customer.to_sql("dim_customer", target_engine, if_exists="append", index=False)
dim_product.to_sql("dim_product", target_engine, if_exists="append", index=False)
dim_store.to_sql("dim_store", target_engine, if_exists="append", index=False)
dim_payment_type.to_sql("dim_payment_type", target_engine, if_exists="append", index=False)
dim_date.to_sql("dim_date", target_engine, if_exists="append", index=False)
fact_order_sales.to_sql("fact_order_sales", target_engine, if_exists="append", index=False)

print("Step 5: Data loaded successfully into retail_olap")
print("Pipeline completed successfully")