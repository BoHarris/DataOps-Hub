import re
import pandas as pd

PII_PATTERNS = {
    "email": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    "ssn": r'\b\d{3}-?\d{2}-\d{4}\b',
    "ip": r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
}

def scan_and_redact_column(series: pd.Series, patterns: dict = PII_PATTERNS) -> pd.Series:
    redacted = series.astype(str)
    for label, regex in patterns.items():
        redacted = redacted.apply(lambda x: "[REDACTED]" if re.search(regex, x) else x)
    return redacted