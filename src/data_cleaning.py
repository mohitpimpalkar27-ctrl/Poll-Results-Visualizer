"""Validate and clean one-answer-per-respondent-per-question data."""
import pandas as pd
from src.data_loader import REQUIRED

KEY = ["respondent_id", "poll_id", "question_id"]

def clean_poll_data(raw):
    df = raw.copy()
    missing = sorted(set(REQUIRED) - set(df.columns))
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    initial = len(df)
    text_columns = [c for c in REQUIRED if c != "response_date"]
    for col in text_columns:
        df[col] = df[col].astype("string").str.strip()
        df[col] = df[col].replace("", pd.NA)
    # Normalize accidental case differences within option labels.
    df["selected_option"] = df["selected_option"].str.lower().str.title()
    df["region"] = df["region"].str.title()
    df["age_group"] = df["age_group"].str.replace(" ", "", regex=False)
    df["response_date"] = pd.to_datetime(df["response_date"], errors="coerce")
    required_not_null = REQUIRED
    df = df.dropna(subset=required_not_null)
    after_missing = len(df)
    df = df.drop_duplicates(subset=KEY, keep="first")
    report = {
        "input_rows": initial,
        "missing_or_invalid_rows_removed": initial - after_missing,
        "duplicate_answers_removed": after_missing - len(df),
        "clean_rows": len(df),
    }
    return df.reset_index(drop=True), report
