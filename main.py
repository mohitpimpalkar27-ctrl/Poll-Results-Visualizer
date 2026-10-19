"""Poll Results Visualizer: interactive Streamlit app."""
from pathlib import Path
import pandas as pd
import streamlit as st
from src.data_generator import generate_poll_data
from src.data_loader import load_csv
from src.data_cleaning import clean_poll_data
from src.poll_analysis import vote_share, segment_analysis, daily_trends
from src.insights import generate_insights
from src.visualizations import interactive_bar, interactive_region, interactive_trend

st.set_page_config(page_title="Poll Results Visualizer", layout="wide")
st.title("📊 Poll Results Visualizer")
st.caption("Synthetic demo data by default • Descriptive analytics, not representative polling")
upload = st.sidebar.file_uploader("Upload a standardized CSV", type=["csv"])
try:
    if upload is not None:
        raw = load_csv(upload)
        origin = "Uploaded CSV"
    elif Path("data/raw/poll_responses.csv").exists():
        raw = load_csv("data/raw/poll_responses.csv")
        origin = "Saved synthetic CSV"
    else:
        raw = generate_poll_data()
        origin = "Generated synthetic demo"
    clean, quality = clean_poll_data(raw)
except (ValueError, pd.errors.ParserError, UnicodeError) as exc:
    st.error(f"Could not read data: {exc}")
    st.stop()

st.sidebar.caption(f"Source: {origin}")
st.sidebar.write("Cleaning report:", quality)
if clean.empty:
    st.warning("No valid responses after cleaning.")
    st.stop()

polls = sorted(clean["poll_id"].unique().tolist())
poll = st.sidebar.selectbox("Poll ID", polls)
base = clean.loc[clean["poll_id"] == poll]
questions = sorted(base["question_id"].unique().tolist())
question = st.sidebar.selectbox("Question ID", questions)
base = base.loc[base["question_id"] == question]
st.subheader(str(base["question"].iloc[0]))

regions = sorted(base["region"].unique().tolist())
ages = sorted(base["age_group"].unique().tolist())
selected_regions = st.sidebar.multiselect("Regions", regions, default=regions)
selected_ages = st.sidebar.multiselect("Age groups", ages, default=ages)
dates = pd.to_datetime(base["response_date"])
min_date, max_date = dates.min().date(), dates.max().date()
date_window = st.sidebar.date_input("Date range", value=(min_date, max_date),
                                   min_value=min_date, max_value=max_date)
if not isinstance(date_window, tuple) or len(date_window) != 2:
    st.info("Select both the start and end dates.")
    st.stop()
start, end = date_window
filtered = base.loc[
    base["region"].isin(selected_regions)
    & base["age_group"].isin(selected_ages)
    & base["response_date"].between(pd.Timestamp(start), pd.Timestamp(end))
].copy()
if filtered.empty:
    st.warning("No responses match the current filters.")
    st.stop()

shares = vote_share(filtered)
c1, c2, c3 = st.columns(3)
c1.metric("Unique respondents", f"{filtered['respondent_id'].nunique():,}")
c2.metric("Valid responses", f"{len(filtered):,}")
c3.metric("Leading option", str(shares.iloc[0]["option"]))
st.plotly_chart(interactive_bar(filtered), use_container_width=True)
left, right = st.columns(2)
with left:
    import plotly.express as px
    st.plotly_chart(px.pie(shares, names="option", values="votes",
                           title="Vote share"), use_container_width=True)
with right:
    st.plotly_chart(interactive_region(filtered), use_container_width=True)
st.plotly_chart(interactive_trend(filtered), use_container_width=True)
st.subheader("Key insights")
for insight in generate_insights(filtered):
    st.write("• " + insight)
st.subheader("Vote summary")
st.dataframe(shares, use_container_width=True)
st.download_button("Download vote summary (CSV)",
                   shares.to_csv(index=False), "vote_summary.csv", "text/csv")
st.download_button("Download filtered records (CSV)",
                   filtered.to_csv(index=False), "filtered_responses.csv", "text/csv")
