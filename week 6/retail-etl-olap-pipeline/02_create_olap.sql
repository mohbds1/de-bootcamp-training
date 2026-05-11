DROP TABLE IF EXISTS fact_order_sales;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_store;
DROP TABLE IF EXISTS dim_payment_type;

CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(120),
    city VARCHAR(80)
);

CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_name VARCHAR(120),
    category VARCHAR(80)
);

CREATE TABLE dim_store (
    store_key INT PRIMARY KEY,
    store_name VARCHAR(100),
    branch_city VARCHAR(80)
);

CREATE TABLE dim_payment_type (
    payment_type_key INT PRIMARY KEY,
    payment_type_name VARCHAR(50)
);

CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_number INT,
    month_number INT,
    month_name VARCHAR(20),
    quarter_number INT,
    year_number INT,
    weekday_name VARCHAR(20),
    is_weekend BOOLEAN,
    is_ramadan BOOLEAN,
    is_eid_al_fitr BOOLEAN,
    is_eid_al_adha BOOLEAN
);

CREATE TABLE fact_order_sales (
    fact_id SERIAL PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    product_key INT REFERENCES dim_product(product_key),
    store_key INT REFERENCES dim_store(store_key),
    payment_type_key INT REFERENCES dim_payment_type(payment_type_key),
    order_id INT,
    quantity INT,
    sales_amount NUMERIC(10,2),
    cost_amount NUMERIC(10,2),
    profit_amount NUMERIC(10,2)
);