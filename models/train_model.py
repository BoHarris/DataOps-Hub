import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.pii_features import extract_column_features

#Step 1: load the column level dataset
df = pd.read_csv("pii_column.csv")

#Step 2: Extract features from column name
df = extract_column_features(df)

#step 3: Define feature matrix and labels
X = df[["length", "num_underscores", "has_at", 
        "has_email_keyword"]]
y = df["is_pii"]

#Step 4: Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X,y, test_size=0.2,random_state=45
)

#Step 5 Train Random Forest model
model = RandomForestClassifier(n_estimators=100,random_state=42, class_weight="balanced")
model.fit(X_train, y_train)

#Step 6: Evaluate and save
accuracy = model.score(X_test, y_test)
print(f"Model trained with accuracy: {accuracy:.2f}")

#Step 7: save model to disk
os.makedirs("models", exist_ok=True)
joblib.dump(model,"models/pii_classifier.pkl" )
print("Model saved to models/pii_classifier.pkl")