import pandas as pd

def calculate_order_metrics(orders, products):

    product_costs = products[
        ["product_id", "cost_price"]
    ]

    df = orders.merge(
        product_costs,
        on="product_id",
        how="left"
    )

    df["gross_revenue"] = (
        df["quantity"] * df["unit_price"]
    )

    df["discount_amount"] = (
        df["gross_revenue"] * df["discount"]
    )

    df["net_revenue"] = (
        df["gross_revenue"] - df["discount_amount"]
    )

    df["total_cost"] = (
        df["quantity"] * df["cost_price"]
    )

    df["profit"] = (
        df["net_revenue"]
        - df["total_cost"]
        - df["shipping_cost"]
    )

    df["profit_margin"] = df["profit" ].div(
    df["net_revenue"].replace(0, pd.NA)
    )

    df["order_value"] = (
        df["net_revenue"] + df["shipping_cost"]
    )
    # cost_price was only needed for calculations.
    # It belongs to the products table, not orders.
    df = df.drop(columns=["cost_price"])
    return df