import os
import sys
import json
import time
import pandas as pd
import schedule
from sqlalchemy import text

# Add current directory to path so db.py can be imported easily
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from db import raw_engine, analytics_engine

STATE_FILE = os.path.join(current_dir, ".pipeline_state.json")
ALLOWED_STATUSES = ["created", "paid", "shipped"]


# Step 1: Ensure clean table exists
def ensure_clean_table():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS clean_orders (
        order_id BIGINT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price DOUBLE PRECISION NOT NULL,
        status TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL,
        processed_at TIMESTAMP NOT NULL DEFAULT NOW()
    );
    """
    with analytics_engine.begin() as conn:
        conn.execute(text(create_table_sql))
    print("Checked analytics table: clean_orders")


# Helper to load the last processed order ID
def load_state():
    if not os.path.exists(STATE_FILE):
        return 0

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            payload = json.loads(file.read())
            return int(payload.get("last_processed_order_id", 0))
    except Exception as e:
        print(f"Error reading state file, starting from 0. Error: {e}")
        return 0


# Helper to save the last processed order ID
def save_state(last_processed_order_id):
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump({"last_processed_order_id": last_processed_order_id}, file, indent=2)


# Step 2: Extract new rows from raw database
def extract_new_rows(last_processed_order_id):
    query = text(
        """
        SELECT order_id, user_id, product_id, quantity, price, status, created_at
        FROM raw_orders
        WHERE order_id > :last_processed_order_id
        ORDER BY order_id ASC;
        """
    )
    with raw_engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"last_processed_order_id": last_processed_order_id})
        return df


# Step 3: Clean and transform the data
def transform_and_clean(df):
    if df.empty:
        return df

    # Work on a copy to avoid warnings
    df = df.copy()
    
    # Convert date strings to actual datetime objects
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    # Apply data validation rules
    clean_df = df[
        (df["quantity"] > 0)
        & (df["price"] > 0)
        & (df["status"].isin(ALLOWED_STATUSES))
        & (df["created_at"].notna())
    ].copy()

    return clean_df


# Step 4: Load clean data into analytics database
def load_clean_data(clean_df):
    if clean_df.empty:
        return

    clean_df.to_sql(
        name="clean_orders",
        con=analytics_engine,
        if_exists="append",
        index=False,
        method="multi",
    )


# Main pipeline process
def run_pipeline_once():
    last_processed_order_id = load_state()
    print(f"--- Starting pipeline run from order_id > {last_processed_order_id} ---")

    try:
        # Extract
        raw_df = extract_new_rows(last_processed_order_id)

        if raw_df.empty:
            print("No new raw orders found.")
            return

        # Transform
        clean_df = transform_and_clean(raw_df)
        
        # Load
        load_clean_data(clean_df)

        # Update state
        new_last_processed = int(raw_df["order_id"].max())
        save_state(new_last_processed)

        print(f"Pipeline finished successfully. Found {len(raw_df)} raw rows, inserted {len(clean_df)} valid rows. New last_processed_id: {new_last_processed}")
    
    except Exception as exc:
        print(f"Pipeline error occurred: {exc}")


def main():
    ensure_clean_table()
    
    # Schedule to run every 1 minute
    schedule.every(1).minutes.do(run_pipeline_once)
    print("Pipeline scheduler started. Running every 1 minute...")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
