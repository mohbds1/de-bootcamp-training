import pandas as pd
import numpy as np

def transform_data(orders_df, order_items_df, payments_df, products_df, translation_df):
    # 1. Merge Orders and Items
    sales = order_items_df.merge(orders_df, on='order_id')
    
    # 2. Join with Payments — aggregate first so multi-payment orders do not duplicate line items / inflate revenue
    payments_agg = payments_df.groupby('order_id').agg({
        'payment_installments': 'max',
        'payment_type': 'first'
    }).reset_index()
    sales = sales.merge(payments_agg, on='order_id')
    
    # 3. Join with Products and Translations
    products = products_df.merge(translation_df, on='product_category_name', how='left')
    sales = sales.merge(products, on='product_id')
    
    # 4. Data Quality: Handle missing values
    sales['product_category_name_english'] = sales['product_category_name_english'].fillna('unknown')
    
    # 5. Create Date Keys
    sales['order_purchase_date_key'] = pd.to_datetime(sales['order_purchase_timestamp']).dt.strftime('%Y%m%d').astype(int)
    
    # 6. Feature Engineering: Total Value
    sales['total_item_value'] = sales['price'] + sales['freight_value']
    
    return sales

def calculate_delivery_performance(orders_df):
    df = orders_df.copy()
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
    df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'])
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    
    # Days to delivery
    df['days_to_delivery'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days
    
    # Is late?
    df['is_late'] = df['order_delivered_customer_date'] > df['order_estimated_delivery_date']

    # Date keys for the warehouse (align with dim_date YYYYMMDD integer keys)
    def _to_date_key(series):
        out = pd.to_numeric(series.dt.strftime('%Y%m%d'), errors='coerce')
        return out.astype('Int64')

    df['purchase_date_key'] = _to_date_key(df['order_purchase_timestamp'])
    df['estimated_delivery_date_key'] = _to_date_key(df['order_estimated_delivery_date'])
    df['actual_delivery_date_key'] = _to_date_key(df['order_delivered_customer_date'])

    return df

if __name__ == "__main__":
    print("ETL Logic Module Initialized.")
