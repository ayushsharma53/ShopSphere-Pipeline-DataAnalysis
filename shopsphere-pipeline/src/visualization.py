import pandas as pd
import matplotlib.pyplot as plt

from src.database import get_engine


def run_query(query):
    engine = get_engine()

    return pd.read_sql(query, engine)\

def monthly_revenue_chart():

    query = """
        SELECT
            DATE_TRUNC('month', order_date) AS month,
            SUM(net_revenue) AS revenue
        FROM orders
        WHERE order_status != 'Cancelled'
          AND order_date IS NOT NULL
        GROUP BY month
        ORDER BY month;
    """

    df = run_query(query)

    df["month"] = pd.to_datetime(
        df["month"]
    ).dt.tz_localize(None)

    plt.figure(figsize=(10, 6))

    plt.plot(
        df["month"],
        df["revenue"],
        marker="o"
    )

    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        "reports/monthly_revenue.png"
    )

    plt.close()

def category_revenue_chart():

    query = """
        SELECT
            p.category,
            SUM(o.net_revenue) AS revenue
        FROM orders o
        JOIN products p
            ON o.product_id = p.product_id
        WHERE o.order_status != 'Cancelled'
        GROUP BY p.category
        ORDER BY revenue DESC;
    """

    df = run_query(query)

    plt.figure(figsize=(10, 6))

    plt.bar(
        df["category"],
        df["revenue"]
    )

    plt.title("Revenue by Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue")

    plt.xticks(rotation=45)
    # use to tilt the text labels on the horizontal x-axis by 45 degrees
    plt.tight_layout()

    plt.savefig(
        "reports/category_revenue.png"
    )

    plt.close()

def regional_revenue_chart():

    query = """
        SELECT
            c.state,
            SUM(o.net_revenue) AS revenue
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        WHERE o.order_status != 'Cancelled'
        GROUP BY c.state
        ORDER BY revenue DESC;
    """

    df = run_query(query)

    plt.figure(figsize=(10, 6))

    plt.bar(
        df["state"],
        df["revenue"]
    )

    plt.title("Revenue by State")
    plt.xlabel("State")
    plt.ylabel("Revenue")

    plt.xticks(rotation=60)
    plt.tight_layout()

    plt.savefig(
        "reports/regional_revenue.png"
    )

    plt.close()
    # We use plt.close() in Matplotlib to completely shut down a figure window and unregister it from the pyplot module. This process permanently destroys the figure object, freeing up system memory.

def top_products_chart():

    query = """
        SELECT
            p.product_name,
            SUM(o.net_revenue) AS revenue
        FROM orders o
        JOIN products p
            ON o.product_id = p.product_id
        WHERE o.order_status != 'Cancelled'
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC
        LIMIT 10;
    """

    df = run_query(query)

    df = df.sort_values("revenue")

    plt.figure(figsize=(10, 6))

    plt.barh(
        df["product_name"],
        df["revenue"]
    )

    plt.title("Top 10 Products by Revenue")
    plt.xlabel("Revenue")
    plt.ylabel("Product")

    plt.tight_layout()

    plt.savefig(
        "reports/top_products.png"
    )

    plt.close()

def sales_channel_chart():

    query = """
        SELECT
            sales_channel,
            SUM(net_revenue) AS revenue
        FROM orders
        WHERE order_status != 'Cancelled'
        GROUP BY sales_channel
        ORDER BY revenue DESC;
    """

    df = run_query(query)

    plt.figure(figsize=(8, 6))

    plt.bar(
        df["sales_channel"],
        df["revenue"]
    )

    plt.title("Revenue by Sales Channel")
    plt.xlabel("Sales Channel")
    plt.ylabel("Revenue")

    plt.tight_layout()

    plt.savefig(
        "reports/sales_channel.png"
    )

    plt.close()

if __name__ == "__main__":

    monthly_revenue_chart()
    category_revenue_chart()
    regional_revenue_chart()
    top_products_chart()
    sales_channel_chart()

    print("All reports generated successfully.")