# 🔐 PII Sentinel – Real-Time PII Detection & Redaction API

PII Sentinel is a FastAPI-based application that uses machine learning and pattern-based detection to identify and redact Personally Identifiable Information (PII) in CSV files.

---

🚀 Features
```
- 📁 Upload CSVs and automatically detect sensitive columns
- 🧠 Predict PII columns using a trained Random Forest classifier
- ✂️ Redact sensitive fields in real time
- 🔎 Uses regex scanning for extra pattern-based redaction
- 🧬 Custom feature engineering to boost PII prediction accuracy
- 🔧 Includes CLI tools and modular design for scalability
- 🪪 Risk scoring: Returns percentage of predicted PII columns
- 📦 Redacted CSV download path returned in every response

---

## ⚙️ Recent Changes (v0.2.0)
```
### ✅ Model & Feature Enhancements
- Added new metadata **and value-based features**:
  - `length`, `num_underscores`, `num_digits`, `has_at`, `has_email_keyword`
  - `pct_email_like`, `pct_phone_like`, `pct_ssn_like`, `pct_ip_like`
  - `avg_digits_per_val`, `avg_val_len`
- Improved model accuracy to **~80–83%** using `class_weight="balanced"`
- Cleaned and expanded training set to include real-world column names and value samples
- Feature importances, correlation matrix, and PII heatmaps added
```
🧠 FastAPI Prediction Improvements
```
- `/predict` now uses both column name and sample values to determine PII
- Extracts first 3 non-null values from each column to match training logic
- Logs predicted column classifications (PII vs non-PII)
- Returns:
  - `filename`
  - `pii_columns`
  - `redacted_file`
  - `risk_score`

🔍 Pattern-Based Redaction
```
- Regex-driven redaction powered by `scan_and_redact_column()`:
  - Emails
  - Phone Numbers
  - SSNs
  - IP Addresses
```
---

## 🛠️ Usage
```
### 1. Train the Model

```bash
python models/train_model.py
Make sure pii_column.csv is present (training data).

2. Run the API
bash
Copy
Edit
uvicorn pii_app:app --reload
Then go to http://127.0.0.1:8000/docs

3. Use /predict
Upload a .csv file. Get back:

✅ Detected PII columns

✂️ Redacted file path

🔒 Risk score
```
🧪 Example Test File
📄 Included test file: test_user_document.csv

📂 Project Structure
```
DataOps Hub/
├── pii_app.py                # FastAPI app
├── models/
│   ├── train_model.py        # Model training
│   └── pii_features.py       # Feature extraction
├── utils/
│   └── redaction.py          # Redaction logic (regex)
├── uploads/                  # Uploaded files
├── redacted/                 # Redacted outputs
├── logs/
│   └── api.log               # Logs for requests
├── test_user_document.csv    # Example CSV for testing
├── CHANGELOG.md              # Feature/version log
├── README.md                 # You’re here
```
🧾 Future Improvements
```
🧠 Prediction UX
Allow users to confirm or override redactions

Add verbose mode to explain why a column was flagged (feature-based reasoning)

🛠️ CLI Tools
--redact flag to redact from terminal

Print risk score and flagged columns

🔍 Client Profiles
Regex rules per client

Support for opt-in sensitivity tiers

📈 Performance Tracking
Track false positives over time

Store confusion matrix with each training run

📁 More Formats
Add .xlsx support

🔐 Privacy Modes
Add differential privacy toggle for pseudonymizing instead of redacting

🧪 Tests & Docs
Add unit/integration tests
```
Improve Swagger docs and upload examples

🤝 Contributing
Ideas, patterns, and use-case-specific suggestions welcome!

Open an issue

Suggest a new pattern

Help tune the model

🧑‍💻 Author
Bo Harris
🔐 Privacy Engineer & Advocate
📫 Contact: Bo.k.harris@gmail.com

📜 License
MIT License © 2025 Bo Harris
