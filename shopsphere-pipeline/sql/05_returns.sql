SELECT
    SUM(refund_amount) AS total_refunds
FROM returns;

SELECT
    return_reason,
    COUNT(*) AS return_count,
    SUM(refund_amount) AS total_refund
FROM returns
GROUP BY return_reason
ORDER BY return_count DESC;

SELECT
    COUNT(DISTINCT r.order_id)::DECIMAL
        / NULLIF(COUNT(DISTINCT o.order_id), 0)
        AS return_rate
FROM orders o
LEFT JOIN returns r
    ON o.order_id = r.order_id
WHERE o.order_status != 'Cancelled';


SELECT
    p.category,
    SUM(r.refund_amount) AS total_refund
FROM returns r
JOIN orders o
    ON r.order_id = o.order_id
JOIN products p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_refund DESC;