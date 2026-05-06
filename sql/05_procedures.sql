DELIMITER //

-- Total by customer using the existing view
DROP PROCEDURE IF EXISTS prc_get_total_by_customer //
CREATE PROCEDURE prc_get_total_by_customer()
BEGIN
    SELECT *
    FROM vw_total_by_customer
    ORDER BY total_value_raw DESC;
END //

-- Search orders by partial customer name
DROP PROCEDURE IF EXISTS prc_get_orders_by_customer //
CREATE PROCEDURE prc_get_orders_by_customer(IN p_customer_name VARCHAR(100))
BEGIN
    SELECT
        order_id,
        formatted_date,
        customer,
        product,
        quantity,
        total_price_formatted
    FROM vw_sales_report
    WHERE customer LIKE CONCAT('%', p_customer_name, '%');
END //

-- Monthly dashboard with key business indicators
DROP PROCEDURE IF EXISTS prc_monthly_dashboard //
CREATE PROCEDURE prc_monthly_dashboard()
BEGIN
    -- KPI 1: Monthly revenue and total orders
    SELECT
        fn_format_currency(SUM(oi.total)) AS monthly_revenue,
        COUNT(DISTINCT o.order_id) AS total_orders
    FROM tb_orders o
    JOIN tb_order_items oi ON oi.order_id = o.order_id
    WHERE o.deleted_at IS NULL
      AND oi.deleted_at IS NULL
      AND MONTH(o.order_date) = MONTH(CURRENT_DATE)
      AND YEAR(o.order_date) = YEAR(CURRENT_DATE);

    -- KPI 2: Revenue by category
    SELECT
        p.category,
        fn_format_currency(SUM(oi.total)) AS revenue
    FROM tb_order_items oi
    JOIN tb_products p ON oi.product_id = p.product_id
    JOIN tb_orders o ON oi.order_id = o.order_id
    WHERE o.deleted_at IS NULL
      AND oi.deleted_at IS NULL
      AND p.deleted_at IS NULL
      AND MONTH(o.order_date) = MONTH(CURRENT_DATE)
      AND YEAR(o.order_date) = YEAR(CURRENT_DATE)
    GROUP BY p.category
    ORDER BY SUM(oi.total) DESC;

    -- KPI 3: Top customer of the month
    SELECT
        c.name AS customer,
        fn_format_currency(SUM(oi.total)) AS total_spent
    FROM tb_customers c
    JOIN tb_orders o ON o.customer_id = c.customer_id
    JOIN tb_order_items oi ON oi.order_id = o.order_id
    WHERE c.deleted_at IS NULL
      AND o.deleted_at IS NULL
      AND oi.deleted_at IS NULL
      AND MONTH(o.order_date) = MONTH(CURRENT_DATE)
      AND YEAR(o.order_date) = YEAR(CURRENT_DATE)
    GROUP BY c.customer_id, c.name
    ORDER BY SUM(oi.total) DESC
    LIMIT 1;
END //

DELIMITER ;