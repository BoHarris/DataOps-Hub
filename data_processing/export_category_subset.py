import pandas as pd
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)


# add logic to export automate data export based on category and condition (senior)
def export_category_subset(dataframe: pd.DataFrame, category: str, export_path: str):
    """Export subset of the data based on category to a new CSV"""
    subset = dataframe[dataframe["Category"] == category]
    subset.to_csv(export_path, index=False)
    print(f"{category} data exported to {export_path}")
