import re
import pandas as pd

PII_PATTERNS = {
    "email": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    "phone": r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
    "ssn": r'\b\d{3}-?\d{2}-\d{4}\b',
    "ip": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    "zip": r'\b\d{5}(?:-\d{4})?\b',
    "dob": r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|(\d{4}[/-]\d{1,2}[/-]\d{1,2})',
}

# Expandable known terms
GENDER_TERMS = {
    "male", "female", "nonbinary", "trans", "woman", "man", "mtf", "ftm", "genderqueer",
    "transgender", "cisgender", "femme", "masculine", "feminine", "neutrois", "intersex", "agender"
}

KNOWN_NAMES = {"alice", "bob", "charlie", "john", "jane"}

CITY_NAMES = {"new york", "los angeles", "miami", "chicago", "jacksonville"}

STREET_SUFFIXES = {
    "st", "street", "ave", "avenue", "road", "rd", "blvd", "ln", "lane",
    "dr", "drive", "ct", "court", "pl", "place", "ter", "terrace", "pkwy", "parkway"
}

def contains_any_term(value: str, term_set: set) -> bool:
    value = value.strip().lower()
    return any(term in value.split() for term in term_set)

def scan_and_redact_column(series: pd.Series) -> pd.Series:
    redacted = series.astype(str)

    def redact_value(val: str) -> str:
        lower_val = val.lower()

        for label, regex in PII_PATTERNS.items():
            if re.search(regex, val):
                return f"[REDACTED_{label.upper()}]"

        if contains_any_term(lower_val, GENDER_TERMS):
            return "[REDACTED_GENDER]"

        if contains_any_term(lower_val, KNOWN_NAMES):
            return "[REDACTED_NAME]"

        if contains_any_term(lower_val, CITY_NAMES):
            return "[REDACTED_CITY]"

        if contains_any_term(lower_val, STREET_SUFFIXES):
            return "[REDACTED_ADDRESS]"

        return val

    return redacted.apply(redact_value)
