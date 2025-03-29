import pandas as pd
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)


def validate_data(dataframe: pd.DataFrame) -> bool:
    if dataframe.isnull().values.any():
        print("Warning: Data contains null values.")
    if not all(dataframe.dtypes == "float64") or (dataframe.dtypes == "int64"):
        print("Warning: Data contains non-numeric types")
    return True
