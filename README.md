# 🔐 PII Sentinel – Real-Time PII Detection & Redaction API

PII Sentinel is a FastAPI-based application that uses machine learning and pattern-based detection to identify and redact Personally Identifiable Information (PII) in CSV files.

## 🚀 Features
```
- 📁 Upload CSVs and automatically detect sensitive columns.
- 🧠 Predict PII columns using a trained Random Forest classifier.
- ✂️ Redact sensitive fields in real time.
- 🔎 Uses regex scanning for extra pattern-based redaction.
- 🔧 Includes CLI tools and modular design for scalability.
- 🧬 Custom feature engineering to boost PII prediction accuracy.
```

## ⚙️ Recent Changes

### ✅ Model and Feature Enhancements
```
- **Added new metadata features for training**:
  - `length`, `num_underscores`, `num_digits`
  - `has_at`, `has_email_keyword`
  - `has_digits_only`, `has_alpha_only`
  - `has_special_chars`, `is_title_case`

- **New feature engineering logic** in `pii_features.py` now captures common patterns in column names that indicate sensitive data.

- **Improved model accuracy** to ~83% with `class_weight="balanced"` and cleaner feature signals.

### 🧠 Prediction Improvements

- **`pii_app.py`** now uses enhanced feature extraction for accurate predictions.
- Predictions are logged to the console (and optionally to logs).
- Integrated both **ML predictions** and **regex-based content scanning**.

### 🔍 Pattern-Based Redaction

- Introduced `scan_and_redact_column()` utility using the following regex patterns:
  - Emails
  - Phone Numbers
  - SSNs
  - IP Addresses

### 🧾 Future Improvements

- Add user input interface to allow:
  - Selecting which detected PII columns to redact
  - Confirming or overriding model predictions
- Create retraining loop with user feedback.

```

## 🛠️ Usage

### 1. Train the Model
```
python models/train_model.py
Ensure your pii_column.csv is present with labeled column names (is_pii column: 0 = PII, 1 = Non-PII).
```
2. Run the API
```
python pii_app.py
Then open your browser at http://127.0.0.1:8000/docs
```
3. Use /predict endpoint
Upload a .csv file

Get back:

Detected PII columns

Redacted file path

Risk score

📂 Project Structure
```
DataOps Hub/
├── pii_app.py                # FastAPI main app
├── models/
│   ├── train_model.py        # Trains the Random Forest model
│   ├── pii_features.py       # Extracts training features
├── utils/
│   └── redaction.py          # Regex scanning and redaction logic
├── uploads/                  # Uploaded CSVs
├── redacted/                 # Redacted output files
├── logs/
│   └── api.log               # Logging API events
├── pii_column.csv            # Labeled training data
```
🤝 Contributing
Ideas, patterns, and use case-specific features are welcome! You can:

Open an issue with feedback

Suggest a new pattern or feature

Help tune the model with better training samples

📜 License
MIT License © 2025 Bo Harris 
