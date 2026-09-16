select sum(net_revenue) as total_revenue
from orders
where orders_status!= 'Cancelled';

SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(net_revenue) AS revenue
FROM orders
WHERE order_status != 'Cancelled'
  AND order_date IS NOT NULL
GROUP BY month
ORDER BY month;

SELECT
    SUM(net_revenue) / COUNT(DISTINCT order_id) AS average_order_value
FROM orders
WHERE order_status != 'Cancelled';

SELECT
    sales_channel,
    SUM(net_revenue) AS revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
WHERE order_status != 'Cancelled'
GROUP BY sales_channel
ORDER BY revenue DESC;