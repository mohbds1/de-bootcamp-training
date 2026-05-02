import os
import pandas as pd
import logging
import sqlite3
import time
from datetime import datetime
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
import etl_logic

_DEFAULT_TARGET_DB_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/ecommerce_dw"

# ==========================================
# 1. Configuration & Logging
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==========================================
# 2. Resiliency: Retry Decorator
# ==========================================
def retry(exceptions, tries=3, delay=2, backoff=2):
    """
    Retry decorator to handle transient failures.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"{e}, Retrying in {mdelay} seconds...")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator

# ==========================================
# 3. ETL Pipeline Class
# ==========================================
class ECommercePipeline:
    def __init__(self, target_db_url=None, source_db_path="olist.sqlite"):
        target_db_url = target_db_url or os.environ.get("DATABASE_URL", _DEFAULT_TARGET_DB_URL)
        # Connect to Target Data Warehouse (PostgreSQL) using SQLAlchemy
        self.target_engine = create_engine(target_db_url)
        try:
            u = make_url(target_db_url)
            logger.info(
                "Connected to Target Data Warehouse (%s://%s:%s/%s)",
                u.drivername,
                u.host,
                u.port or "",
                u.database,
            )
        except Exception:
            logger.info("Connected to Target Data Warehouse (URL configured)")
        
        # Connect to Source Database (SQLite)
        self.source_db_path = source_db_path
        try:
            self.source_conn = sqlite3.connect(self.source_db_path)
            logger.info(f"Connected to Source OLTP Database ({source_db_path})")
        except Exception as e:
            logger.error(f"Failed to connect to source: {e}")

    @retry(Exception, tries=3)
    def extract_from_source(self, table_name):
        """
        Extracts data from the source SQLite database.
        """
        logger.info(f"Extracting data from source table: {table_name}...")
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, self.source_conn)
        logger.info(f"Successfully extracted {len(df)} rows from {table_name}.")
        return df

    def load_to_bronze(self, df, table_name):
        """
        Loads raw data into the Bronze (Staging) layer in PostgreSQL.
        """
        df['ingested_at'] = datetime.now()
        df.to_sql(f"bronze_{table_name}", self.target_engine, if_exists='replace', index=False)
        logger.info(f"Loaded {len(df)} rows to bronze_{table_name}")

    def transform_silver(self):
        """
        Performs cleaning, deduplication, and standardization using pandas logic.
        """
        logger.info("Starting Silver Layer transformation...")
        try:
            logger.info("Fetching Bronze tables...")
            orders_df = pd.read_sql("SELECT * FROM bronze_orders", self.target_engine)
            order_items_df = pd.read_sql("SELECT * FROM bronze_order_items", self.target_engine)
            products_df = pd.read_sql("SELECT * FROM bronze_products", self.target_engine)
            translation_df = pd.read_sql("SELECT * FROM bronze_product_category_name_translation", self.target_engine)
            
            customers_df = pd.read_sql("SELECT * FROM bronze_customers", self.target_engine)
            # Remove duplicate customers based on customer_id
            customers_silver = customers_df.drop_duplicates(subset=['customer_id'])
            customers_silver.to_sql("silver_customers", self.target_engine, if_exists='replace', index=False)
            logger.info(f"Loaded {len(customers_silver)} rows to silver_customers")

            payments_df = pd.read_sql("SELECT * FROM bronze_order_payments", self.target_engine)

            logger.info("Transforming Sales Data...")
            sales_silver = etl_logic.transform_data(orders_df, order_items_df, payments_df, products_df, translation_df)
            sales_silver.to_sql("silver_sales", self.target_engine, if_exists='replace', index=False)
            logger.info(f"Loaded {len(sales_silver)} rows to silver_sales")

            logger.info("Calculating Delivery Performance...")
            delivery_silver = etl_logic.calculate_delivery_performance(orders_df)
            delivery_silver.to_sql("silver_delivery", self.target_engine, if_exists='replace', index=False)
            logger.info(f"Loaded {len(delivery_silver)} rows to silver_delivery")

            logger.info("Silver transformation completed successfully.")

        except Exception as e:
            logger.error(f"Error during Silver transformation: {str(e)}")
            raise
    def load_gold(self):
        """
        Loads data into the final Star Schema (Gold Layer).
        """
        logger.info("Starting Gold Layer load (Star Schema)...")
        from sqlalchemy import text
        
        try:
            with self.target_engine.begin() as conn:
                logger.info("Clearing old Gold data and preparing partitions...")
                conn.execute(text("TRUNCATE TABLE fact_sales, fact_delivery CASCADE;"))
                conn.execute(text("TRUNCATE TABLE dim_customers, dim_products, dim_sellers, dim_date CASCADE;"))
                
                conn.execute(text("CREATE TABLE IF NOT EXISTS fact_sales_default PARTITION OF fact_sales DEFAULT;"))

                logger.info("Loading Dimension Tables...")
                # 1. Dim Customers
                conn.execute(text("""
                    INSERT INTO dim_customers (customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state)
                    SELECT customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state 
                    FROM silver_customers;
                """))
                
                # 2. Dim Sellers
                conn.execute(text("""
                    INSERT INTO dim_sellers (seller_id, seller_zip_code_prefix, seller_city, seller_state)
                    SELECT seller_id, seller_zip_code_prefix, seller_city, seller_state 
                    FROM bronze_sellers;
                """))

                # 3. Dim Products
                conn.execute(text("""
                    INSERT INTO dim_products (product_id, product_category_name, product_category_name_english, product_weight_g, product_length_cm, product_height_cm, product_width_cm)
                    SELECT p.product_id, p.product_category_name, t.product_category_name_english, p.product_weight_g, p.product_length_cm, p.product_height_cm, p.product_width_cm 
                    FROM bronze_products p
                    LEFT JOIN bronze_product_category_name_translation t ON p.product_category_name = t.product_category_name;
                """))

                # 4. Dim Date
                conn.execute(text("""
                    INSERT INTO dim_date (
                        date_key, full_date, day_of_week, day_name,
                        month, month_name, quarter, year, day_type
                    )
                    SELECT
                        to_char(dt, 'YYYYMMDD')::INT,
                        dt::DATE,
                        EXTRACT(DOW FROM dt)::INT,
                        TRIM(TO_CHAR(dt::DATE, 'Day')),
                        EXTRACT(MONTH FROM dt)::INT,
                        TRIM(TO_CHAR(dt::DATE, 'Month')),
                        EXTRACT(QUARTER FROM dt)::INT,
                        EXTRACT(YEAR FROM dt)::INT,
                        CASE WHEN EXTRACT(DOW FROM dt) IN (0,6) THEN 'Weekend' ELSE 'Weekday' END
                    FROM generate_series(
                        (SELECT MIN(TO_DATE(order_purchase_date_key::TEXT, 'YYYYMMDD')) FROM silver_sales),
                        (SELECT MAX(TO_DATE(actual_delivery_date_key::TEXT, 'YYYYMMDD')) FROM silver_delivery),
                        '1 day'::INTERVAL
                    ) AS dt
                    ;
                """))

                logger.info("Loading Fact Tables...")
                # 5. Fact Sales
                conn.execute(text("""
                    INSERT INTO fact_sales (
                        order_id, customer_key, product_key, seller_key,
                        order_purchase_date_key, price, freight_value,
                        payment_installments, payment_type
                    )
                    SELECT 
                        s.order_id, c.customer_key, p.product_key, sl.seller_key,
                        s.order_purchase_date_key, s.price, s.freight_value,
                        s.payment_installments, s.payment_type
                    FROM silver_sales s
                    JOIN dim_customers c ON s.customer_id = c.customer_id
                    JOIN dim_products p ON s.product_id = p.product_id
                    JOIN dim_sellers sl ON s.seller_id = sl.seller_id;
                """))

                # 6. Fact Delivery
                conn.execute(text("""
                    INSERT INTO fact_delivery (
                        order_id,
                        customer_key,
                        purchase_date_key,
                        estimated_delivery_date_key,
                        actual_delivery_date_key,
                        days_to_delivery,
                        is_late
                    )
                    SELECT
                        d.order_id,
                        c.customer_key,
                        d.purchase_date_key,
                        d.estimated_delivery_date_key,
                        d.actual_delivery_date_key,
                        d.days_to_delivery,
                        d.is_late
                    FROM silver_delivery d
                    JOIN dim_customers c ON d.customer_id = c.customer_id;
                """))

            logger.info("Gold Layer load completed successfully!")
        except Exception as e:
            logger.error(f"Error during Gold load: {str(e)}")
            raise

    def run_pipeline(self):
        """
        Orchestrates the full ETL process.
        """
        try:
            start_time = time.time()
            logger.info("Pipeline Execution Started.")
            
            source_tables = [
                'orders', 
                'order_items', 
                'customers', 
                'products', 
                'sellers',
                'product_category_name_translation',
                'order_payments' 
            ]
            
            for table in source_tables:
                df = self.extract_from_source(table)
                self.load_to_bronze(df, table)
            
            self.transform_silver()

            self.load_gold()
            
            duration = time.time() - start_time
            logger.info(f"Pipeline Execution Finished. Duration: {duration:.2f}s")
            
        except Exception as e:
            logger.error(f"Pipeline Failed: {str(e)}")
            raise
if __name__ == "__main__":
    pipeline = ECommercePipeline()
    pipeline.run_pipeline() 