SELECT
    c.customer_id,
    c.name,
    COUNT(DISTINCT o.order_id) AS number_of_orders,
    SUM(o.net_revenue) AS total_revenue,
    SUM(o.profit) AS total_profit
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_status != 'Cancelled'
GROUP BY
    c.customer_id,
    c.name
ORDER BY total_revenue DESC
LIMIT 10;

SELECT
    c.customer_id,
    c.name,
    COUNT(DISTINCT o.order_id) AS purchase_frequency
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_status != 'Cancelled'
GROUP BY
    c.customer_id,
    c.name
ORDER BY purchase_frequency DESC;

SELECT
    c.customer_id,
    c.name,
    MAX(o.order_date) AS last_order_date
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.name
HAVING
    MAX(o.order_date) < CURRENT_DATE - INTERVAL '180 days'
    OR MAX(o.order_date) IS NULL
ORDER BY last_order_date;