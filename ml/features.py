import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.feature_selection import SelectKBest, mutual_info_classif


def encode_data_type(dataframe: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Encode a categorical column using Label Encoding"""
    label_encoder = LabelEncoder()
    dataframe[f"{column_name}_encoded"] = label_encoder.fit_transform(
        dataframe[column_name]
    )
    return dataframe


def normalize_feature(dataframe: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Normalize a numerical column to the range [0,1]"""
    scaler = MinMaxScaler()
    dataframe[columns] = scaler.fit_transform(dataframe[columns])
    return dataframe


def select_feature(
    dataframe: pd.DataFrame, target_column: str, k: int = 3
) -> pd.DataFrame:
    """Select top K features based on mutual information with the target column"""
    X = dataframe.drop(columns=[target_column])
    y = dataframe[target_column]
    selector = SelectKBest(mutual_info_classif, k=k)
    X_new = selector.fit_transform(X, y)
    selected_columns = X.columns[selector.get_support()]
    print("Selected features:\n", selected_columns)
    return X_new, y, selected_columns


def prepare_features(dataframe):
    """Perform encoding, normalization, and selection of key features"""
    # Encode categorical column like "Sex"
    if "Sex" in dataframe.columns:
        dataframe["Sex"] = LabelEncoder().fit_transform(dataframe["Sex"])

    # Encode 'data_type' if it exists in dataset
    if "data_type" in dataframe.columns:
        dataframe = encode_data_type(dataframe, "data_type")
    else:
        print("Warning: 'data_type' column not found in dataset")

    # Normalize specific columns
    dataframe = normalize_feature(dataframe, ["Fare", "Normalized_Age"])

    # Select relevant columns for X and y
    X = dataframe[["Pclass", "Sex", "SibSp", "Parch", "Fare", "Normalized_Age"]]
    y = dataframe["Survived"]  # Assuming 'Survived' is the target column for this model

    # Featire selection
    selected_columns = X.columns = X.columns.tolist()

    return X, y, selected_columns
