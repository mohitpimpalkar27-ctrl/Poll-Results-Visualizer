import pandas as pd
from src.poll_analysis import vote_share, segment_analysis
from src.data_cleaning import clean_poll_data
from src.data_generator import generate_poll_data

def test_vote_share():
    df = pd.DataFrame({"selected_option": ["Python", "Python", "Java", "Java", "Java"]})
    result = vote_share(df).set_index("option")
    assert result.loc["Java", "votes"] == 3
    assert result.loc["Python", "percentage"] == 40.0

def test_region_percentages():
    df = pd.DataFrame({
        "region": ["Mumbai", "Mumbai", "Pune"],
        "selected_option": ["Python", "Java", "Python"]
    })
    result = segment_analysis(df)
    assert result.loc[(result.region == "Pune"), "percentage"].iloc[0] == 100

def test_generator_cleaning():
    df = generate_poll_data(100, seed=42)
    clean, report = clean_poll_data(df)
    assert len(clean) == 100
    assert report["duplicate_answers_removed"] == 0
    assert clean["poll_id"].nunique() == 5
