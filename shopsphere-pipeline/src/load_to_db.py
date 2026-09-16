from src.database import get_engine


def load_dataframe(df, table_name):
    engine = get_engine()

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(df)} rows into {table_name}")