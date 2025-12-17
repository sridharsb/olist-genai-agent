# db/setup_db.py

import duckdb
import os

# ---------------------------
# Paths
# ---------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_DIR = os.path.join(BASE_DIR, "db")
DB_PATH = os.path.join(DB_DIR, "olist.db")

os.makedirs(DB_DIR, exist_ok=True)

con = duckdb.connect(DB_PATH)

print("📦 Creating Olist database at:", DB_PATH)

# ---------------------------
# 1️⃣ Load raw tables
# ---------------------------

tables = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "products": "olist_products_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

for table, file in tables.items():
    path = os.path.join(DATA_DIR, file)
    print(f"➡️ Loading {table}")
    con.execute(f"""
        CREATE OR REPLACE TABLE {table} AS
        SELECT * FROM read_csv_auto('{path}')
    """)

# ---------------------------
# 2️⃣ Fix timestamp columns
# ---------------------------

print("⏱ Fixing timestamp types")

con.execute("""
    ALTER TABLE orders
    ALTER COLUMN order_purchase_timestamp
    SET DATA TYPE TIMESTAMP
""")

# ---------------------------
# 3️⃣ CORE FACT VIEW
# ---------------------------

print("📊 Creating core fact view")

con.execute("""
CREATE OR REPLACE VIEW v_order_facts AS
SELECT
    o.order_id,
    o.customer_id,
    o.order_purchase_timestamp,
    p.product_id,
    COALESCE(p.product_category_name, 'Unknown') AS category,
    oi.seller_id,
    pay.payment_type,
    pay.payment_value,
    r.review_score,
    c.customer_state,
    s.seller_state
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN payments pay ON o.order_id = pay.order_id
LEFT JOIN reviews r ON o.order_id = r.order_id
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN sellers s ON oi.seller_id = s.seller_id
""")

# ---------------------------
# 4️⃣ REVENUE & SALES VIEWS
# ---------------------------

print("💰 Revenue & sales views")

# Revenue by category
con.execute("""
CREATE OR REPLACE VIEW v_category_revenue AS
SELECT
    category,
    SUM(payment_value) AS revenue
FROM v_order_facts
GROUP BY category
""")

# Revenue by category & year
con.execute("""
CREATE OR REPLACE VIEW v_category_year_revenue AS
SELECT
    EXTRACT(YEAR FROM order_purchase_timestamp) AS year,
    category,
    SUM(payment_value) AS revenue
FROM v_order_facts
GROUP BY year, category
""")

# Monthly revenue
con.execute("""
CREATE OR REPLACE VIEW v_monthly_revenue AS
SELECT
    strftime('%Y-%m', order_purchase_timestamp) AS year_month,
    SUM(payment_value) AS revenue
FROM v_order_facts
GROUP BY year_month
ORDER BY year_month
""")

# ---------------------------
# 5️⃣ PRODUCT & CATEGORY PERFORMANCE
# ---------------------------

print("📦 Product & category performance")

# Category units sold
con.execute("""
CREATE OR REPLACE VIEW v_category_units_sold AS
SELECT
    category,
    COUNT(*) AS units_sold
FROM v_order_facts
GROUP BY category
""")

# Product performance
con.execute("""
CREATE OR REPLACE VIEW v_product_performance AS
SELECT
    product_id,
    category,
    COUNT(*) AS units_sold,
    SUM(payment_value) AS revenue,
    AVG(review_score) AS avg_rating
FROM v_order_facts
GROUP BY product_id, category
""")

# ---------------------------
# 6️⃣ CUSTOMER ANALYTICS
# ---------------------------

print("👤 Customer analytics")

# Customer lifetime value
con.execute("""
CREATE OR REPLACE VIEW v_customer_ltv AS
SELECT
    customer_id,
    customer_state,
    SUM(payment_value) AS lifetime_value,
    COUNT(DISTINCT order_id) AS total_orders
FROM v_order_facts
GROUP BY customer_id, customer_state
""")

# ---------------------------
# 7️⃣ SELLER ANALYTICS
# ---------------------------

print("🏪 Seller analytics")

con.execute("""
CREATE OR REPLACE VIEW v_seller_performance AS
SELECT
    seller_id,
    seller_state,
    SUM(payment_value) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    AVG(review_score) AS avg_rating
FROM v_order_facts
GROUP BY seller_id, seller_state
""")

# ---------------------------
# 8️⃣ PAYMENT ANALYTICS
# ---------------------------

print("💳 Payment analytics")

con.execute("""
CREATE OR REPLACE VIEW v_payment_analysis AS
SELECT
    payment_type,
    COUNT(DISTINCT order_id) AS orders,
    SUM(payment_value) AS revenue,
    AVG(payment_value) AS avg_payment
FROM payments
GROUP BY payment_type
""")

# ---------------------------
# 9️⃣ TIME INTELLIGENCE
# ---------------------------

print("📅 Time intelligence")

# Yearly revenue
con.execute("""
CREATE OR REPLACE VIEW v_yearly_revenue AS
SELECT
    EXTRACT(YEAR FROM order_purchase_timestamp) AS year,
    SUM(payment_value) AS revenue
FROM v_order_facts
GROUP BY year
ORDER BY year
""")

# order category reveneue
con.execute("""
CREATE OR REPLACE VIEW v_order_category_revenue AS
SELECT
    o.order_id,
    p.product_category_name AS category,
    SUM(oi.price + oi.freight_value) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY o.order_id, p.product_category_name
""")

#derived view
con.execute("""
CREATE OR REPLACE VIEW v_category_aov AS
SELECT
    category,
    ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM v_order_category_revenue
GROUP BY category
""")

# ---------------------------
# DONE
# ---------------------------

print("✅ Database setup complete with analytics views")
print("📐 Order value metrics")

# Average Order Value (AOV)
con.execute("""
CREATE OR REPLACE VIEW v_order_value_metrics AS
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(payment_value) AS total_revenue,
    ROUND(
        SUM(payment_value) / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS average_order_value
FROM v_order_facts
""")
con.execute("""
CREATE OR REPLACE VIEW v_category_aov AS
SELECT
    category,
    ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM v_order_category_revenue
GROUP BY category
""")

con.close()
