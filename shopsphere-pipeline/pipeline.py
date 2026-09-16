from pathlib import Path

from src.ingestion import load_csv, get_dataset_stats
from src.cleaning import (
    clean_customers,
    clean_products,
    clean_orders,
    clean_returns,
    validate_order_references,
    remove_invalid_order_references,
    remove_invalid_return_references
)
from src.tranformation import calculate_order_metrics
from src.load_to_db import load_dataframe

DATA_DIR = Path("shopsphere_raw_data/data/raw")


def main():
   
    # -------------------------
    # 1. INGESTION
    # -------------------------

    datasets = {}

    for name in ["customers", "products", "orders", "returns"]:

        path = DATA_DIR / f"{name}.csv"

        print(f"\nLoading {name}...")

        df = load_csv(path)

        datasets[name] = df
        # datasets = {"customers" : df["customer"],etc}

        stats = get_dataset_stats(df)

        print(f"Rows: {stats['rows']}")
        print(f"Columns: {stats['columns']}")
        print(f"Duplicate rows: {stats['duplicate_rows']}")
        print(f"Missing values: {stats['missing_values']}")

    # -------------------------
    # 2. CLEANING
    # -------------------------

    print("\n========== CLEANING ==========")

    datasets["customers"] = clean_customers(
        datasets["customers"]
    )

    datasets["products"] = clean_products(
        datasets["products"]
    )

    datasets["orders"] = clean_orders(
        datasets["orders"]
    )

    datasets["returns"] = clean_returns(
        datasets["returns"]
    )

    datasets["orders"] = remove_invalid_order_references(
    datasets["orders"],
    datasets["customers"],
    datasets["products"]
    )

    datasets["returns"] = remove_invalid_return_references(
    datasets["returns"],
    datasets["orders"]
    )
    # -------------------------
    # 3. QUALITY CHECK AFTER CLEANING
    # -------------------------

    print("\n========== AFTER CLEANING ==========")

    for name, df in datasets.items():

        stats = get_dataset_stats(df)

        print(f"\n{name}")

        print(f"Rows: {stats['rows']}")
        print(f"Duplicate rows: {stats['duplicate_rows']}")
        print(f"Missing values: {stats['missing_values']}")
        invalid_customers, invalid_products = validate_order_references(
            datasets["orders"],
            datasets["customers"],
            datasets["products"]
        )
        
        print(
            f"\nOrders with invalid customer IDs: "
            f"{len(invalid_customers)}"
        )
        
        print(
            f"Orders with invalid product IDs: "
            f"{len(invalid_products)}"
        )

    # -------------------------
    # 4.Transformation
    # -------------------------
    print("\n========== TRANSFORMATION ==========")

    datasets["orders"] = calculate_order_metrics(
        datasets["orders"],
        datasets["products"]
    )

    print("Order metrics calculated.")
    print(
        datasets["orders"][
            [
                "order_id",
                "gross_revenue",
                "net_revenue",
                "profit",
                "profit_margin",
                "order_value"
            ]
        ].head()
    )
    print("\nInfinite values:")
    print(
        datasets["orders"]
        .select_dtypes(include="number")
        .isin([float("inf"), float("-inf")])
        .sum()
        )

    print("\nMissing transformed values:")
    print(
        datasets["orders"][
            [
                "gross_revenue",
                "discount_amount",
                "net_revenue",
                "total_cost",
                "profit",
                "profit_margin",
                "order_value"
            ]
        ].isnull().sum()
    )
    print("\n========== DATABASE LOADING ==========")

    load_dataframe(datasets["customers"], "customers")
    load_dataframe(datasets["products"], "products")
    load_dataframe(datasets["orders"], "orders")
    load_dataframe(datasets["returns"], "returns")

if __name__ == "__main__":
    main()

# The line if __name__ == "__main__": main() is a standard Python boilerplate template used to control what code runs when a script is executed.It ensures that the main() function only runs when you run the file directly, but not if you import it into another file.