-- Postgres compatible procedures script for Neon

-- 1. Total by customer using the existing view
CREATE OR REPLACE FUNCTION prc_get_total_by_customer()
RETURNS TABLE(
    customer_name VARCHAR(100),
    total_orders BIGINT,
    total_value_raw NUMERIC,
    total_value_formatted VARCHAR(30)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM vw_total_by_customer
    ORDER BY total_value_raw DESC;
END;
$$;

-- 2. Search orders by partial customer name
CREATE OR REPLACE FUNCTION prc_get_orders_by_customer(p_customer_name VARCHAR(100))
RETURNS TABLE(
    order_id INT,
    formatted_date VARCHAR(20),
    customer VARCHAR(100),
    product VARCHAR(100),
    quantity INT,
    total_price_formatted VARCHAR(30)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        v.order_id,
        v.formatted_date,
        v.customer,
        v.product,
        v.quantity,
        v.total_price_formatted
    FROM vw_sales_report v
    WHERE v.customer ILIKE CONCAT('%', p_customer_name, '%');
END;
$$;

-- 3. Monthly dashboard with key business indicators returning multiple refcursors
CREATE OR REPLACE PROCEDURE prc_monthly_dashboard(
    INOUT summary REFCURSOR DEFAULT 'summary',
    INOUT categories REFCURSOR DEFAULT 'categories',
    INOUT top_customer REFCURSOR DEFAULT 'top_customer'
)
LANGUAGE plpgsql
AS $$
BEGIN
    OPEN summary FOR
        SELECT
            fn_format_currency(SUM(oi.total)) AS monthly_revenue,
            COUNT(DISTINCT o.order_id) AS total_orders
        FROM tb_orders o
        JOIN tb_order_items oi ON oi.order_id = o.order_id
        WHERE o.deleted_at IS NULL
          AND oi.deleted_at IS NULL
          AND o.order_date >= date_trunc('month', CURRENT_DATE)
          AND o.order_date < date_trunc('month', CURRENT_DATE) + INTERVAL '1 month';

    OPEN categories FOR
        SELECT
            p.category,
            fn_format_currency(SUM(oi.total)) AS revenue
        FROM tb_order_items oi
        JOIN tb_products p ON oi.product_id = p.product_id
        JOIN tb_orders o ON oi.order_id = o.order_id
        WHERE o.deleted_at IS NULL
          AND oi.deleted_at IS NULL
          AND p.deleted_at IS NULL
          AND o.order_date >= date_trunc('month', CURRENT_DATE)
          AND o.order_date < date_trunc('month', CURRENT_DATE) + INTERVAL '1 month'
        GROUP BY p.category
        ORDER BY SUM(oi.total) DESC;

    OPEN top_customer FOR
        SELECT
            c.name AS customer,
            fn_format_currency(SUM(oi.total)) AS total_spent
        FROM tb_customers c
        JOIN tb_orders o ON o.customer_id = c.customer_id
        JOIN tb_order_items oi ON oi.order_id = o.order_id
        WHERE c.deleted_at IS NULL
          AND o.deleted_at IS NULL
          AND oi.deleted_at IS NULL
          AND o.order_date >= date_trunc('month', CURRENT_DATE)
          AND o.order_date < date_trunc('month', CURRENT_DATE) + INTERVAL '1 month'
        GROUP BY c.customer_id, c.name
        ORDER BY SUM(oi.total) DESC
        LIMIT 1;
END;
$$;