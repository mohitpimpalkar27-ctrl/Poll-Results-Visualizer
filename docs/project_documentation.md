# Technical Notes

## Pipeline
CSV / synthetic generator → schema validation → cleaning → filter one poll and question → vote shares and demographic breakdown → charts and descriptive insights → exports.

## Denominator
Overall percentage = option votes / all valid responses for that question × 100.
Region percentage = option votes in region / all valid responses in that region × 100.

## Cleaning decisions
Invalid dates and missing required values are excluded. Duplicate answers are removed using respondent_id + poll_id + question_id. Option labels are case-normalized. The raw CSV is retained.

## Reproducibility
The synthetic generator uses a fixed NumPy random seed. Regional and age effects are intentionally injected and do not represent real-world preferences.

## Limits
No weighting, confidence intervals, causal inference, multi-select support, or automatic conversion of wide Google Forms exports.
