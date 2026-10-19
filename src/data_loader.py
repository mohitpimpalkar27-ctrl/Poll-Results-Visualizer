"""CSV loader with schema checks."""
import pandas as pd

REQUIRED = [
    "respondent_id", "response_date", "poll_id", "question_id",
    "question", "selected_option", "region", "age_group"
]

def load_csv(source):
    df = pd.read_csv(source, dtype={c: "string" for c in REQUIRED if c != "response_date"})
    missing = sorted(set(REQUIRED) - set(df.columns))
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    if df.empty:
        raise ValueError("CSV has no records.")
    return df
