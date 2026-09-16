SELECT
    c.state,
    SUM(o.net_revenue) AS revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_status != 'Cancelled'
GROUP BY c.state
ORDER BY revenue DESC;


SELECT
    c.state,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_status != 'Cancelled'
GROUP BY c.state
ORDER BY total_orders DESC;


SELECT
    c.state,
    SUM(o.net_revenue)
        / NULLIF(COUNT(DISTINCT o.order_id), 0)
        AS average_order_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_status != 'Cancelled'
GROUP BY c.state
ORDER BY average_order_value DESC;
