import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.pii_features import extract_column_features

#Step 1: load the column level dataset
df = pd.read_csv("../pii_column.csv")

#step 2 map PII to numeric values
df["is_pii"] = df["pii"].map({"yes": 0, "no": 1}) #note 0 =PII

#Step 3: Extract features from column name
df = extract_column_features(df)

#add features
features = ["length", "num_underscores", "num_digits", "has_at",
            "has_email_keyword", "pct_email_like", "pct_phone_like", 
            "pct_ssn_like", "pct_ip_like", "avg_digits_per_val","avg_val_len"]

X=df[features]
y=df["is_pii"]

#Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#train model
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X_train, y_train)

#Evaluate model
preds = model.predict(X_test)
print(classification_report(y_test, preds))
print(f"Accuracy: {accuracy_score(y_test, preds)}")

#Save model
joblib.dump(model, "xgboost_model.pkl")
print("Model saved to xgboost_model.pkl")