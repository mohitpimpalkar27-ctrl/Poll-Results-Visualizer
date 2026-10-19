"""Reproducible synthetic single-choice survey responses (NOT real opinions)."""
from pathlib import Path
import numpy as np
import pandas as pd

POLL_CONFIG = {
    "P001": ("Preferred programming language", ["Python", "Java", "JavaScript", "C++", "Other"]),
    "P002": ("Preferred learning platform", ["YouTube", "Coursera", "Udemy", "College", "Other"]),
    "P003": ("Employee satisfaction", ["Very satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very dissatisfied"]),
    "P004": ("Most important product feature", ["Battery", "Camera", "Performance", "Price", "Display"]),
    "P005": ("Workshop rating", ["Excellent", "Good", "Average", "Poor", "Very poor"]),
}
REGIONS = ["Mumbai", "Pune", "Thane", "Nashik"]
AGES = ["18-24", "25-34", "35-44", "45+"]
BASE_WEIGHTS = {
    "P001": [0.43, 0.25, 0.16, 0.11, 0.05],
    "P002": [0.38, 0.22, 0.19, 0.16, 0.05],
    "P003": [0.18, 0.37, 0.25, 0.14, 0.06],
    "P004": [0.30, 0.20, 0.18, 0.23, 0.09],
    "P005": [0.29, 0.39, 0.21, 0.08, 0.03],
}

def generate_poll_data(n=5000, seed=42):
    """One row = one respondent answering one single-choice question."""
    rng = np.random.default_rng(seed)
    records = []
    for i in range(n):
        poll_id = f"P{(i % 5) + 1:03d}"
        question, options = POLL_CONFIG[poll_id]
        region = str(rng.choice(REGIONS, p=[0.40, 0.25, 0.23, 0.12]))
        age = str(rng.choice(AGES, p=[0.45, 0.32, 0.16, 0.07]))
        weights = np.array(BASE_WEIGHTS[poll_id], dtype=float)
        # Small intentionally simulated differences between groups.
        if region == "Pune":
            weights[1] += 0.07
        if age == "18-24":
            weights[0] += 0.06
        weights /= weights.sum()
        selected = str(rng.choice(options, p=weights))
        date = pd.Timestamp("2026-08-01") + pd.Timedelta(days=int(rng.integers(0, 75)))
        records.append({
            "respondent_id": f"R{i+1:05d}",
            "response_date": date.strftime("%Y-%m-%d"),
            "poll_id": poll_id, "question_id": "Q001",
            "question": question, "selected_option": selected,
            "region": region, "age_group": age,
            "source": "Synthetic"
        })
    return pd.DataFrame(records)

def save_synthetic_data(path="data/raw/poll_responses.csv", n=5000, seed=42):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df = generate_poll_data(n=n, seed=seed)
    df.to_csv(path, index=False)
    return df

if __name__ == "__main__":
    df = save_synthetic_data()
    print(f"Generated {len(df)} synthetic records")
