-- Reporting Layer Queries

-- 1. How are sales trending over time?
SELECT 
    d.year, 
    d.month, 
    SUM(f.price + f.freight_value) as total_revenue,
    COUNT(DISTINCT f.order_id) as total_orders
FROM fact_sales f
JOIN dim_date d ON f.order_purchase_date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 2. Who are the most valuable customers?
-- (Using customer_unique_id to track the same person across different orders)
SELECT 
    c.customer_unique_id,
    COUNT(DISTINCT f.order_id) as total_orders,
    SUM(f.price + f.freight_value) as lifetime_value
FROM fact_sales f
JOIN dim_customers c ON f.customer_key = c.customer_key
GROUP BY c.customer_unique_id
ORDER BY lifetime_value DESC
LIMIT 10;

-- 3. Seller-based delivery performance
-- One order can have many line items; join at (order_id, seller_key) so metrics are not duplicated per item.
SELECT 
    s.seller_state,
    AVG(d.days_to_delivery) as avg_delivery_days,
    COUNT(DISTINCT d.order_id) as total_orders,
    100.0 * COUNT(DISTINCT CASE WHEN d.is_late THEN d.order_id END)
        / NULLIF(COUNT(DISTINCT d.order_id), 0) as late_delivery_rate
FROM fact_delivery d
JOIN (
    SELECT DISTINCT order_id, seller_key
    FROM fact_sales
) ord_sellers ON d.order_id = ord_sellers.order_id
JOIN dim_sellers s ON ord_sellers.seller_key = s.seller_key
GROUP BY s.seller_state
ORDER BY late_delivery_rate DESC;

-- 4. Which products/categories drive revenue?
SELECT 
    p.product_category_name_english,
    SUM(f.price + f.freight_value) as total_revenue,
    COUNT(f.order_item_id) as units_sold
FROM fact_sales f
JOIN dim_products p ON f.product_key = p.product_key
GROUP BY p.product_category_name_english
ORDER BY total_revenue DESC;

-- 5. Customer-based delivery experience
SELECT
    c.customer_state,
    AVG(d.days_to_delivery) as avg_delivery_days,
    COUNT(DISTINCT d.order_id) as total_orders,
    100.0 * COUNT(DISTINCT CASE WHEN d.is_late THEN d.order_id END)
        / NULLIF(COUNT(DISTINCT d.order_id), 0) as late_delivery_rate
FROM fact_delivery d
JOIN dim_customers c ON d.customer_key = c.customer_key
GROUP BY c.customer_state
ORDER BY late_delivery_rate DESC;
