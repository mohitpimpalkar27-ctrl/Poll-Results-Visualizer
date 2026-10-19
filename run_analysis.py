"""Run complete offline pipeline and save CSVs and charts."""
from pathlib import Path
from src.data_generator import save_synthetic_data
from src.data_loader import load_csv
from src.data_cleaning import clean_poll_data
from src.poll_analysis import vote_share, segment_analysis, daily_trends
from src.visualizations import save_charts
from src.insights import generate_insights

def main():
    raw_path = Path("data/raw/poll_responses.csv")
    if not raw_path.exists():
        save_synthetic_data(raw_path)
    raw = load_csv(raw_path)
    clean, quality = clean_poll_data(raw)
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    Path("outputs").mkdir(parents=True, exist_ok=True)
    clean.to_csv("data/processed/cleaned_poll_data.csv", index=False)
    # One selected question only: avoid mixing incompatible option sets.
    first_poll = sorted(clean["poll_id"].unique())[0]
    selected = clean[(clean["poll_id"] == first_poll) &
                     (clean["question_id"] == "Q001")].copy()
    vote_share(selected).to_csv("outputs/summary_statistics.csv", index=False)
    segment_analysis(selected, "region").to_csv("outputs/region_analysis.csv", index=False)
    segment_analysis(selected, "age_group").to_csv("outputs/age_group_analysis.csv", index=False)
    daily_trends(selected).to_csv("outputs/trend_analysis.csv", index=False)
    charts = save_charts(selected)
    report = [f"Cleaning report: {quality}", f"Poll: {first_poll}",
              *generate_insights(selected)]
    Path("outputs/insights.txt").write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))
    print(f"Saved {len(charts)} charts in outputs/charts/")

if __name__ == "__main__":
    main()
