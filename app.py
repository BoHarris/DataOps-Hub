# Flask API for model deployment
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Set the model path to root directory
model_path = os.path.join(os.getcwd(), "model.pkl")

# Check if the model file exists and load it
if os.path.exists(model_path):
    model = joblib.load(model_path)
    print(f"Model loaded from {model_path}")
else:
    print("model.pkl not found at the specified path.")
    exit(1)  # Exit if model file is not found


@app.route("/predict", methods=["POST"])
def predict():
    # Get data from the POST request and convert it to a DataFrame
    data = request.get_json()
    df = pd.DataFrame([data])

    # Rename columns to match the training data's feature names
    df = df.rename(
        columns={
            "age": "Age",
            "income_normalized": "Fare",
            "education_encoded": "Pclass",
        }
    )

    # Generate prediction using the loaded model
    prediction = model.predict(df)

    # Return the prediction as JSON
    return jsonify({"prediction": int(prediction[0])})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
