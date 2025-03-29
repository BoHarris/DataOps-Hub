import pandas as pd
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)


def load_data(filepath: str) -> pd.DataFrame:
    """Load a CSV file into a Dataframe"""
    logging.info(f"Loading data from {filepath}")
    try:
        df = pd.read_csv(filepath)
        logging.info(f"Loaded data with shape: {df.shape}")
        return df
    except Exception as e:
        logging.error(f"Error loading data: {e}")
    return pd.DataFrame()
