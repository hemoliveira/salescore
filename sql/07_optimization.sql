-- Postgres compatible optimization script for Neon

-- Less efficient / legacy style query (old implicit join syntax)
SELECT
    oi.item_id,
    oi.order_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    oi.total,
    o.order_date,
    c.customer_id,
    c.name
FROM tb_order_items oi, tb_orders o, tb_customers c
WHERE oi.order_id = o.order_id
  AND o.customer_id = c.customer_id
  AND oi.deleted_at IS NULL
  AND o.deleted_at IS NULL
  AND c.deleted_at IS NULL;

-- Optimized query for reporting workloads
SELECT
    c.customer_id,
    c.name,
    SUM(oi.total) AS total_spent
FROM tb_customers c
INNER JOIN tb_orders o
    ON o.customer_id = c.customer_id
INNER JOIN tb_order_items oi
    ON oi.order_id = o.order_id
WHERE c.deleted_at IS NULL
  AND o.deleted_at IS NULL
  AND oi.deleted_at IS NULL
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;

-- Execution plan for the optimized query
EXPLAIN
SELECT
    c.customer_id,
    c.name,
    SUM(oi.total) AS total_spent
FROM tb_customers c
INNER JOIN tb_orders o
    ON o.customer_id = c.customer_id
INNER JOIN tb_order_items oi
    ON oi.order_id = o.order_id
WHERE c.deleted_at IS NULL
  AND o.deleted_at IS NULL
  AND oi.deleted_at IS NULL
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;