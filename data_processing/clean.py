import pandas as pd
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)


def clean_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean the data handling missing values, removing duplicates and parsing dates"""
    # Handle missing values in Age column
    if "Age" in dataframe.columns:
        median_age = dataframe["Age"].median()
        dataframe["Age"] = dataframe["Age"].fillna(median_age)
        # Ensure ages are within a reasonable range
        dataframe["Age"] = dataframe["Age"].apply(
            lambda x: x if 0 <= x <= 120 else None
        )
        dataframe.drop_duplicates(inplace=True)
        return dataframe
