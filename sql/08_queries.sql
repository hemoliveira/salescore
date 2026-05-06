-- 1. Total spent by each customer
SELECT
    customer_name,
    total_value_raw,
    total_value_formatted AS total
FROM vw_total_by_customer
ORDER BY total_value_raw DESC, customer_name ASC;

-- 2. Total quantity sold by product
SELECT
    p.product_id,
    p.name,
    SUM(oi.quantity) AS total_qty
FROM tb_order_items oi
JOIN tb_products p
    ON p.product_id = oi.product_id
JOIN tb_orders o
    ON o.order_id = oi.order_id
WHERE o.deleted_at IS NULL
  AND oi.deleted_at IS NULL
  AND p.deleted_at IS NULL
GROUP BY
    p.product_id,
    p.name
ORDER BY total_qty DESC, p.name ASC;

-- 3. Monthly sales totals (numeric for charts)
SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS sales_month,
    YEAR(o.order_date) AS year_num,
    MONTH(o.order_date) AS month_num,
    SUM(oi.total) AS total_raw
FROM tb_orders o
JOIN tb_order_items oi
    ON oi.order_id = o.order_id
WHERE o.deleted_at IS NULL
  AND oi.deleted_at IS NULL
GROUP BY
    DATE_FORMAT(o.order_date, '%Y-%m'),
    YEAR(o.order_date),
    MONTH(o.order_date)
ORDER BY sales_month;

-- 4. Monthly sales totals (formatted for reports)
SELECT
    DATE_FORMAT(o.order_date, '%M %Y') AS month_label,
    fn_format_currency(SUM(oi.total)) AS total_formatted
FROM tb_orders o
JOIN tb_order_items oi
    ON oi.order_id = o.order_id
WHERE o.deleted_at IS NULL
  AND oi.deleted_at IS NULL
GROUP BY
    DATE_FORMAT(o.order_date, '%Y-%m'),
    DATE_FORMAT(o.order_date, '%M %Y')
ORDER BY DATE_FORMAT(o.order_date, '%Y-%m');

-- 5. Total sales by product category
SELECT
    p.category,
    SUM(oi.total) AS total_raw,
    fn_format_currency(SUM(oi.total)) AS total_category
FROM tb_products p
JOIN tb_order_items oi
    ON p.product_id = oi.product_id
JOIN tb_orders o
    ON o.order_id = oi.order_id
WHERE p.deleted_at IS NULL
  AND o.deleted_at IS NULL
  AND oi.deleted_at IS NULL
GROUP BY
    p.category
ORDER BY total_raw DESC, p.category ASC;

-- 6. Detailed audit log
SELECT
    *
FROM vw_audit_report;