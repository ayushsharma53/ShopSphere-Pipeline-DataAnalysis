import pandas as pd
from pathlib import Path


def load_csv(path):
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.stat().st_size == 0:
        raise ValueError(f"File is empty: {file_path}")

    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        raise ValueError(f"CSV contains no data: {file_path}")
    except pd.errors.ParserError:
        raise ValueError(f"Malformed CSV file: {file_path}")

    if df.empty:
        raise ValueError(f"Dataset contains no rows: {file_path}")

    return df


def validate_columns(df, required_columns):
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return True


def get_dataset_stats(df):
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum())
    }