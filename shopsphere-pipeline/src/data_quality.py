from pandas.api.types import is_numeric_dtype

def check_missing_values(df):
    return df.isnull().sum()

def check_duplicates(df):
    return df.diplicated().sum()

def check_duplicate_ids(df, id_column):
    return df[id_column].duplicated().sum()

def check_invalid_numeric(df, column, min_value=0):
    if df[column] <= min_value:
        raise ValueError(f"Invalid")
# You cannot use a Pandas DataFrame (df) or Series directly in a standard Python if-else statement because Python's if statement expects a single truth value (either True or False), whereas a DataFrame or Series contains multiple elements, resulting in an array of boolean values
    return df[df[column]<= min_value]
def check_invalid_categories(df, column, allowed_values):
    # check = df[column].isin(allowed_values)
    # if check:
    #     raise ValueError(f"Invalid")
    return df[df[column].isin(allowed_values)]
        

def check_referential_integrity(
    child_df,
    child_column,
    parent_df,
    parent_column
):
   
    valid_ids = set(parent_df(parent_column).dropna())
    return child_df[child_df[child_column].isin(valid_ids)]