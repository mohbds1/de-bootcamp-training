-- Data Warehouse DDL Script (PostgreSQL)

-- ==========================================
-- DIMENSION TABLES
-- ==========================================

CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_of_week INT,
    day_name VARCHAR(10),
    month INT,
    month_name VARCHAR(10),
    quarter INT,
    year INT,
    day_type VARCHAR(10)
);

CREATE TABLE dim_customers (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state CHAR(2)
);

CREATE TABLE dim_products (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50),
    product_category_name VARCHAR(100),
    product_category_name_english VARCHAR(100),
    product_weight_g DECIMAL,
    product_length_cm DECIMAL,
    product_height_cm DECIMAL,
    product_width_cm DECIMAL
);

CREATE TABLE dim_sellers (
    seller_key SERIAL PRIMARY KEY,
    seller_id VARCHAR(50),
    seller_zip_code_prefix INT,
    seller_city VARCHAR(100),
    seller_state CHAR(2)
);

-- ==========================================
-- FACT TABLES
-- ==========================================

-- Fact Sales (Grain: Order Item)
CREATE TABLE fact_sales (
    order_item_id SERIAL,
    order_id VARCHAR(50),
    customer_key INT REFERENCES dim_customers(customer_key),
    product_key INT REFERENCES dim_products(product_key),
    seller_key INT REFERENCES dim_sellers(seller_key),
    order_purchase_date_key INT NOT NULL REFERENCES dim_date(date_key),
    price DECIMAL(10,2),
    freight_value DECIMAL(10,2),
    payment_installments INT,
    payment_type VARCHAR(20),
    PRIMARY KEY (order_item_id, order_purchase_date_key)
) PARTITION BY RANGE (order_purchase_date_key);

-- Fact Delivery (Grain: Order)
CREATE TABLE fact_delivery (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_key INT REFERENCES dim_customers(customer_key),
    purchase_date_key INT REFERENCES dim_date(date_key),
    estimated_delivery_date_key INT,
    actual_delivery_date_key INT,
    delivery_status VARCHAR(20),
    days_to_delivery INT,
    is_late BOOLEAN
);

-- Fact Leads (Grain: Closed Lead)
CREATE TABLE fact_leads (
    mql_id VARCHAR(50) PRIMARY KEY,
    seller_key INT REFERENCES dim_sellers(seller_key),
    won_date_key INT REFERENCES dim_date(date_key),
    business_segment VARCHAR(100),
    lead_type VARCHAR(50),
    declared_monthly_revenue DECIMAL(15,2)
);

-- ==========================================
-- INDEXES FOR PERFORMANCE
-- ==========================================
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_key);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_key);
CREATE INDEX idx_fact_sales_date ON fact_sales(order_purchase_date_key);
CREATE INDEX idx_fact_delivery_status ON fact_delivery(delivery_status);
