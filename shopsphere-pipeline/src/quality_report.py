from pathlib import Path

from src.ingestion import load_csv
from src.data_quality import (
    check_missing_values,
    check_duplicates,
    check_duplicate_ids,
    check_invalid_numeric,
    check_invalid_categories,
    check_referential_integrity
)


DATA_DIR = Path("data/raw")


def main():

    customers = load_csv(DATA_DIR / "customers.csv")
    products = load_csv(DATA_DIR / "products.csv")
    orders = load_csv(DATA_DIR / "orders.csv")
    returns = load_csv(DATA_DIR / "returns.csv")

    print("\n" + "=" * 50)
    print("SHOPSPHERE DATA QUALITY REPORT")
    print("=" * 50)

    # ---------------- CUSTOMERS ----------------

    print("\nCUSTOMERS")
    print("-" * 30)

    print("Rows:", len(customers))
    print(
        "Duplicate IDs:",
        check_duplicate_ids(customers, "customer_id")
    )
    # When Python executes your code, it runs the function first. The function calculates the data and returns a pandas object. The brackets then operate on that returned object, not on the function name itself.

    print("\nMissing values:")
    print(
        check_missing_values(customers)[
            check_missing_values(customers) > 0
        ]
    )

    # ---------------- PRODUCTS ----------------

    print("\nPRODUCTS")
    print("-" * 30)

    print("Rows:", len(products))
    print(
        "Duplicate IDs:",
        check_duplicate_ids(products, "product_id")
    )

    invalid_product_prices = check_invalid_numeric(
        products,
        "selling_price"
    )

    print(
        "Invalid selling prices:",
        len(invalid_product_prices)
    )

    # ---------------- ORDERS ----------------

    print("\nORDERS")
    print("-" * 30)

    print("Rows:", len(orders))

    print(
        "Duplicate IDs:",
        check_duplicate_ids(orders, "order_id")
    )

    print("\nMissing values:")
    print(
        check_missing_values(orders)[
            check_missing_values(orders) > 0
        ]
    )

    invalid_quantities = check_invalid_numeric(
        orders,
        "quantity"
    )

    print(
        "Invalid quantities:",
        len(invalid_quantities)
    )

    invalid_prices = check_invalid_numeric(
        orders,
        "unit_price"
    )

    print(
        "Invalid prices:",
        len(invalid_prices)
    )

    allowed_statuses = {
        "Completed",
        "Pending",
        "Cancelled",
        "Returned"
    }

    invalid_statuses = check_invalid_categories(
        orders,
        "order_status",
        allowed_statuses
    )

    print(
        "Invalid statuses:",
        len(invalid_statuses)
    )

    invalid_customers = check_referential_integrity(
        orders,
        "customer_id",
        customers,
        "customer_id"
    )

    print(
        "Invalid customer references:",
        len(invalid_customers)
    )

    invalid_products = check_referential_integrity(
        orders,
        "product_id",
        products,
        "product_id"
    )

    print(
        "Invalid product references:",
        len(invalid_products)
    )

    # ---------------- RETURNS ----------------

    print("\nRETURNS")
    print("-" * 30)

    print("Rows:", len(returns))

    print(
        "Duplicate IDs:",
        check_duplicate_ids(returns, "return_id")
    )

    invalid_refunds = check_invalid_numeric(
        returns,
        "refund_amount"
    )

    print(
        "Invalid refund amounts:",
        len(invalid_refunds)
    )

    invalid_return_orders = check_referential_integrity(
        returns,
        "order_id",
        orders,
        "order_id"
    )

    print(
        "Invalid order references:",
        len(invalid_return_orders)
    )


if __name__ == "__main__":
    main()