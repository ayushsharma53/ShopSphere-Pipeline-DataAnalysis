import pandas as pd

def clean_customers(df):
    df = df.copy()

    df["name"] = df["name"].str.strip()
    # df["name"] is a Pandas Series object.df["name"].str exposes all the string manipulation tools for that Series.df["name"].str.strip() performs the actual cleaning on every row.
    df["city"] = df["city"].str.strip()
    df["state"] = df["state"].str.strip().str.title()

    # Normalize email
    df["email"] = df["email"].str.strip().str.lower()

    # Convert signup_date to datetime
    df["signup_date"] = pd.to_datetime(
        df["signup_date"],
        errors="coerce"
    )
    # Yes, numeric data is technically stored as text (strings) in a CSV file.
    # Remove duplicate customer IDs
    df = df.drop_duplicates(
        subset=["customer_id"],
        keep="first"
    )

    return df

def clean_products(df):

    df = df.copy()

    df["product_name"] = df["product_name"].str.strip()
    df["category"] = df["category"].str.strip().str.title()
    df["subcategory"] = df["subcategory"].str.strip().str.title()
    df["supplier"] = df["supplier"].str.strip()

    # Numeric conversion
    df["cost_price"] = pd.to_numeric(
        df["cost_price"],
        errors="coerce"
    )

    df["selling_price"] = pd.to_numeric(
        df["selling_price"],
        errors="coerce"
    )

    # Remove duplicate product IDs
    df = df.drop_duplicates(
        subset=["product_id"],
        keep="first"
    )
        # Invalid prices
    df.loc[df["cost_price"] < 0, "cost_price"] = pd.NA

    df.loc[df["selling_price"] < 0, "selling_price"] = pd.NA

    return df

def clean_orders(df):

    df = df.copy()

    # Normalize categorical columns
    df["payment_method"] = df["payment_method"].str.strip().str.title()
    df["sales_channel"] = df["sales_channel"].str.strip().str.title()
    df["order_status"] = df["order_status"].str.strip().str.title()

    # Convert dates
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    # Convert numeric fields
    numeric_columns = [
        "quantity",
        "unit_price",
        "discount",
        "shipping_cost"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove duplicate order IDs
    df = df.drop_duplicates(
        subset=["order_id"],
        keep="first"
    )

        # Invalid quantity
    df.loc[df["quantity"] <= 0, "quantity"] = pd.NA
    # The line df.loc[df["quantity"] <= 0, "quantity"] = pd.NA finds all rows where the "quantity" column is zero or negative and replaces those values with Pandas' native missing value marker (pd.NA).
   
    # Invalid unit price
    df.loc[df["unit_price"] < 0, "unit_price"] = pd.NA

    # Discount must be between 0 and 1
    df.loc[
        (df["discount"] < 0) | (df["discount"] > 1),
        "discount"
    ] = pd.NA

    # Shipping cost cannot be negative
    df.loc[
        df["shipping_cost"] < 0,
        "shipping_cost"
    ] = pd.NA

    return df


def clean_returns(df):

    df = df.copy()

    df["return_date"] = pd.to_datetime(
        df["return_date"],
        errors="coerce"
    )

    df["return_reason"] = df["return_reason"].str.strip().str.title()

    df["refund_amount"] = pd.to_numeric(
        df["refund_amount"],
        errors="coerce"
    )

    df = df.drop_duplicates(
        subset=["return_id"],
        keep="first"
    )

    return df

def validate_order_references(orders, customers, products):

    valid_customers = set(
        customers["customer_id"].dropna()
    )

    valid_products = set(
        products["product_id"].dropna()
    )

    invalid_customers = orders[
        ~orders["customer_id"].isin(valid_customers)
    ]

    invalid_products = orders[
        ~orders["product_id"].isin(valid_products)
    ]

    return invalid_customers, invalid_products

def remove_invalid_order_references(orders, customers, products):

    df = orders.copy()

    valid_customer_ids = set(
        customers["customer_id"].dropna()
    )

    valid_product_ids = set(
        products["product_id"].dropna()
    )

    invalid_customer = ~df["customer_id"].isin(
        valid_customer_ids
    )

    invalid_product = ~df["product_id"].isin(
        valid_product_ids
    )

    invalid_rows = invalid_customer | invalid_product

    print(
        f"Orders with invalid customer references: "
        f"{invalid_customer.sum()}"
    )

    print(
        f"Orders with invalid product references: "
        f"{invalid_product.sum()}"
    )

    print(
        f"Total orders removed due to invalid references: "
        f"{invalid_rows.sum()}"
    )

    return df[~invalid_rows].copy()

def remove_invalid_return_references(returns, orders):

    df = returns.copy()

    valid_order_ids = set(
        orders["order_id"].dropna()
    )

    invalid_returns = ~df["order_id"].isin(
        valid_order_ids
    )

    print(
        f"Returns with invalid order references: "
        f"{invalid_returns.sum()}"
    )

    return df[~invalid_returns].copy()