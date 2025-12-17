"""
SQL TEMPLATES FOR OLIST ANALYTICS AGENT
-------------------------------------
✔ Uses ONLY analytics views
✔ No raw tables
✔ No placeholders
✔ DuckDB safe
✔ Works with rule + LLM intent detection
"""

SQL_TEMPLATES = {

    # ==================================================
    # 📈 REVENUE ANALYTICS
    # ==================================================

    "highest_revenue_category": """
        SELECT category, revenue
        FROM v_category_revenue
        ORDER BY revenue DESC
        LIMIT 1
    """,

    "lowest_revenue_category": """
        SELECT category, revenue
        FROM v_category_revenue
        ORDER BY revenue ASC
        LIMIT 1
    """,

    "revenue_by_category": """
        SELECT category, revenue
        FROM v_category_revenue
        ORDER BY revenue DESC
    """,

    "category_revenue_by_year": """
        SELECT year, category, revenue
        FROM v_category_year_revenue
        ORDER BY year, revenue DESC
    """,

    "yearly_revenue": """
        SELECT year, revenue
        FROM v_yearly_revenue
        ORDER BY year
    """,

    "monthly_revenue_trend": """
        SELECT year_month, revenue
        FROM v_monthly_revenue
        ORDER BY year_month
    """,

    # ==================================================
    # 📦 SALES / UNITS ANALYTICS
    # ==================================================

    "most_selling_category": """
        SELECT category, units_sold
        FROM v_category_units_sold
        ORDER BY units_sold DESC
        LIMIT 1
    """,

    "least_selling_category": """
        SELECT category, units_sold
        FROM v_category_units_sold
        ORDER BY units_sold ASC
        LIMIT 1
    """,

    "units_by_category": """
        SELECT category, units_sold
        FROM v_category_units_sold
        ORDER BY units_sold DESC
    """,

    # ==================================================
    # 🛍 PRODUCT ANALYTICS
    # ==================================================

    "top_products_by_revenue": """
        SELECT product_id, category, revenue
        FROM v_product_performance
        ORDER BY revenue DESC
        LIMIT 10
    """,

    "top_products_by_units": """
        SELECT product_id, category, units_sold
        FROM v_product_performance
        ORDER BY units_sold DESC
        LIMIT 10
    """,

    "product_performance": """
        SELECT
            product_id,
            category,
            revenue,
            units_sold,
            avg_rating
        FROM v_product_performance
        ORDER BY revenue DESC
    """,

    # ==================================================
    # 👤 CUSTOMER ANALYTICS
    # ==================================================

    "customer_lifetime_value": """
        SELECT
            customer_state,
            SUM(lifetime_value) AS total_ltv
        FROM v_customer_ltv
        GROUP BY customer_state
        ORDER BY total_ltv DESC
    """,

    "top_customers": """
        SELECT
            customer_id,
            lifetime_value
        FROM v_customer_ltv
        ORDER BY lifetime_value DESC
        LIMIT 10
    """,

    # ==================================================
    # 🏪 SELLER ANALYTICS
    # ==================================================

    "top_sellers_by_revenue": """
        SELECT
            seller_id,
            seller_state,
            revenue
        FROM v_seller_performance
        ORDER BY revenue DESC
        LIMIT 10
    """,

    "seller_performance": """
        SELECT
            seller_state,
            revenue,
            avg_rating
        FROM v_seller_performance
        ORDER BY revenue DESC
    """,

    # ==================================================
    # 💳 PAYMENT ANALYTICS
    # ==================================================

    "payment_type_analysis": """
        SELECT
            payment_type,
            orders,
            revenue,
            avg_payment
        FROM v_payment_analysis
        ORDER BY revenue DESC
    """,

    # ==================================================
    # 📐 ORDER VALUE ANALYTICS
    # ==================================================

    "average_order_value": """
        SELECT
        total_orders,
        total_revenue,
        average_order_value
    FROM v_order_value_metrics
    """,


    "average_order_value_by_category": """
        SELECT
            category,
            average_order_value
    FROM v_category_aov
    ORDER BY average_order_value DESC
    """
}
