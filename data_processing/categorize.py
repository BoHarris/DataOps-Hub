import pandas as pd
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)


def categorize_age(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe["Category"] = dataframe["Age"].apply(
        lambda x: "Senior" if x > 50 else "Adult"
    )
    return dataframe
