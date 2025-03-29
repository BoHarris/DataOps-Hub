import pandas as pd


def create_compliance_lables(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Generate lables for compliance based on given rules"""
    # Define compliance based rule
    if "sensitive_data" in dataframe.columns:
        dataframe["compliance_label"] = dataframe["sensitive_data"].apply(
            lambda x: 1 if x == "high" else 0
        )
    else:
        print("Warning: 'Sensitive_data' column not found for labeling compliance.")
    return dataframe
