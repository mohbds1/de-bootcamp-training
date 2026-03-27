import os
import random
import time
from datetime import datetime

import schedule
from faker import Faker
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

fake = Faker()
ALLOWED_STATUSES = ["created", "paid", "shipped"]

# Database connection settings
RAW_DB_CONFIG = {
    "host": os.getenv("RAW_DB_HOST", "localhost"),
    "port": int(os.getenv("RAW_DB_PORT", "5432")),
    "dbname": os.getenv("RAW_DB_NAME", "db_raw"),
    "user": os.getenv("RAW_DB_USER", "postgres"),
    "password": os.getenv("RAW_DB_PASSWORD", "123"),
}


# Connect to the raw database
def get_connection():
    return psycopg2.connect(**RAW_DB_CONFIG, cursor_factory=RealDictCursor)


# Create table if it doesn't exist
def create_table_if_not_exists():
    query = """
    CREATE TABLE IF NOT EXISTS raw_orders (
        order_id BIGSERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price DOUBLE PRECISION NOT NULL,
        status TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL
    );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
    print("Checked raw table: db_raw.raw_orders")


# Generate a random order
def generate_order():
    return {
        "user_id": fake.random_int(min=1, max=500),
        "product_id": fake.random_int(min=1, max=1000),
        "quantity": fake.random_int(min=1, max=10),
        "price": round(fake.pyfloat(min_value=5.0, max_value=500.0, right_digits=2), 2),
        "status": random.choice(ALLOWED_STATUSES),
        "created_at": datetime.now(),
    }


# Insert the generated order into the database
def insert_order(order):
    query = """
    INSERT INTO raw_orders (user_id, product_id, quantity, price, status, created_at)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (
                    order["user_id"],
                    order["product_id"],
                    order["quantity"],
                    order["price"],
                    order["status"],
                    order["created_at"],
                ),
            )
        conn.commit()


# The scheduled job
def job():
    order = generate_order()
    insert_order(order)
    print(f"Inserted new raw order: {order}")


def main():
    create_table_if_not_exists()
    
    # Schedule the job every 1 second
    schedule.every(1).seconds.do(job)
    print("Order generator started. Inserting one order every second...")

    while True:
        schedule.run_pending()
        time.sleep(0.2)


if __name__ == "__main__":
    main()