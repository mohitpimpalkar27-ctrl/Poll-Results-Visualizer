# Poll Results Visualizer

A reproducible **synthetic survey analytics** project using Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, and Streamlit.

## Features
- 5 simulated single-choice polls; 5,000 synthetic response records
- CSV import (standard schema), validation, deduplication and cleaning
- Option vote counts and shares
- Region/age-group comparisons, daily trends
- PNG exports, CSV summaries and interactive dashboard
- Rule-based descriptive insights and automated tests

## Setup
```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run
```bash
python -m src.data_generator
python run_analysis.py
python -m pytest -q
streamlit run main.py
```

The dashboard opens in your browser. Use the sidebar to filter or upload a CSV.

## CSV schema
`respondent_id,response_date,poll_id,question_id,question,selected_option,region,age_group`

Dates should be `YYYY-MM-DD`. Each row represents **one response to one single-choice question**. For a single-choice question, `(respondent_id, poll_id, question_id)` is unique. Google Forms exports generally need their columns transformed into this long format before upload.

## Outputs
- `data/raw/poll_responses.csv`: reproducible synthetic responses
- `data/processed/cleaned_poll_data.csv`: cleaned data
- `outputs/*.csv`: summaries for poll P001, question Q001
- `outputs/charts/*.png`: static figures
- `outputs/insights.txt`: narrative observations

## Interpretation and limitations
All supplied demo data are synthetic and not representative of any population. Counts and shares are descriptive; they are **not** election forecasts, confidence intervals, or causal conclusions. No respondent PII is required. Multiple-choice and survey weighting are out of scope.

## Screenshots
After launching, save your screenshots to `images/` and add them here:
- Dashboard overview
- Option-wise bar and pie charts
- Region comparison
- Daily response trends
- Filters and downloaded CSV

## Technology
Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit, Pytest.

