import pandas as pd

def extract_column_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Extract key metadata features from column names for PII detection."""
    dataframe["length"] = dataframe["column"].apply(len)
    dataframe["num_underscores"] = dataframe["column"].apply(lambda x: x.count("_"))
    dataframe["num_digits"] = dataframe["column"].apply(lambda x: sum(c.isdigit() for c in x))
    dataframe["has_at"] = dataframe["column"].apply(lambda x: int("@" in x))
    dataframe["has_email_keyword"] = dataframe["column"].apply(lambda x: int("email" in x.lower()))
    return dataframe