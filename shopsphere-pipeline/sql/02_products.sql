SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.net_revenue) AS revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
WHERE o.order_status != 'Cancelled'
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY revenue DESC
LIMIT 10;


SELECT
    p.product_id,
    p.product_name,
    SUM(o.profit) AS total_profit
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
WHERE o.order_status != 'Cancelled'
GROUP BY
    p.product_id,
    p.product_name
ORDER BY total_profit DESC
LIMIT 10;


SELECT
    p.category,
    SUM(o.profit) / NULLIF(SUM(o.net_revenue), 0)
        AS profit_margin
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
WHERE o.order_status != 'Cancelled'
GROUP BY p.category
ORDER BY profit_margin DESC;