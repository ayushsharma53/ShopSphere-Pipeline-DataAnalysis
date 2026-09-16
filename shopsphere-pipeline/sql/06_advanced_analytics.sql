WITH product_revenue AS (
    SELECT
        p.category,
        p.product_id,
        p.product_name,
        SUM(o.net_revenue) AS revenue
    FROM orders o
    JOIN products p
        ON o.product_id = p.product_id
    WHERE o.order_status != 'Cancelled'
    GROUP BY
        p.category,
        p.product_id,
        p.product_name
),

ranked_products AS (
    SELECT
        *,
        RANK() OVER (
            PARTITION BY category
            ORDER BY revenue DESC
        ) AS category_rank
    FROM product_revenue
)

SELECT *
FROM ranked_products
WHERE category_rank <= 3
ORDER BY category, category_rank;



WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        SUM(net_revenue) AS revenue
    FROM orders
    WHERE order_status != 'Cancelled'
    GROUP BY month
),

previous_month AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (
            ORDER BY month
        ) AS previous_revenue
    FROM monthly_revenue
)

SELECT
    month,
    revenue,
    previous_revenue,
    revenue - previous_revenue AS revenue_change,
    ROUND(
        (
            (revenue - previous_revenue)
            / NULLIF(previous_revenue, 0)
        ) * 100,
        2
    ) AS growth_percentage
FROM previous_month
ORDER BY month;




WITH customer_revenue AS (
    SELECT
        c.customer_id,
        c.name,
        COALESCE(SUM(o.net_revenue), 0) AS revenue
    FROM customers c
    LEFT JOIN orders o
        ON c.customer_id = o.customer_id
        AND o.order_status != 'Cancelled'
    GROUP BY
        c.customer_id,
        c.name
)

SELECT
    customer_id,
    name,
    revenue,
    CASE
        WHEN revenue >= 100000 THEN 'High Value'
        WHEN revenue >= 50000 THEN 'Medium Value'
        WHEN revenue > 0 THEN 'Low Value'
        ELSE 'No Purchase'
    END AS customer_segment
FROM customer_revenue
ORDER BY revenue DESC;



WITH customer_revenue AS (
    SELECT
        customer_id,
        SUM(net_revenue) AS revenue
    FROM orders
    WHERE order_status != 'Cancelled'
    GROUP BY customer_id
)

SELECT
    customer_id,
    revenue
FROM customer_revenue
WHERE revenue > (
    SELECT AVG(revenue)
    FROM customer_revenue
)
ORDER BY revenue DESC;



WITH product_orders AS (
    SELECT
        product_id,
        COUNT(DISTINCT order_id) AS total_orders
    FROM orders
    WHERE order_status != 'Cancelled'
    GROUP BY product_id
),

product_returns AS (
    SELECT
        o.product_id,
        COUNT(DISTINCT r.order_id) AS returned_orders
    FROM returns r
    JOIN orders o
        ON r.order_id = o.order_id
    GROUP BY o.product_id
)

SELECT
    p.product_id,
    p.product_name,
    po.total_orders,
    COALESCE(pr.returned_orders, 0) AS returned_orders,
    ROUND(
        COALESCE(pr.returned_orders, 0)::DECIMAL
        / NULLIF(po.total_orders, 0) * 100,
        2
    ) AS return_rate
FROM products p
JOIN product_orders po
    ON p.product_id = po.product_id
LEFT JOIN product_returns pr
    ON p.product_id = pr.product_id
WHERE
    COALESCE(pr.returned_orders, 0)::DECIMAL
    / NULLIF(po.total_orders, 0) > 0.10
ORDER BY return_rate DESC;