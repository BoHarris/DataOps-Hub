import pandas as pd
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)


# Aggregate data
def aggregate_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Aggregate data by Category, calculating summary statics for each group."""
    # category by the "Category" column and calculate summary stastics for each group.
    return dataframe.groupby("Category").agg({"Age": ["mean", "min", "max", "std"]})
