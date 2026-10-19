"""Descriptive analysis of one selected single-choice question."""
import pandas as pd

def vote_share(df):
    if df.empty:
        return pd.DataFrame(columns=["option", "votes", "percentage"])
    counts = df["selected_option"].value_counts()
    result = counts.rename_axis("option").reset_index(name="votes")
    result["percentage"] = (100 * result["votes"] / result["votes"].sum()).round(2)
    return result

def segment_analysis(df, segment="region"):
    if segment not in ("region", "age_group"):
        raise ValueError("Segment must be region or age_group")
    if df.empty:
        return pd.DataFrame(columns=[segment, "selected_option", "votes", "segment_total", "percentage"])
    grouped = (df.groupby([segment, "selected_option"], observed=True)
               .size().reset_index(name="votes"))
    grouped["segment_total"] = grouped.groupby(segment)["votes"].transform("sum")
    grouped["percentage"] = (100 * grouped["votes"] / grouped["segment_total"]).round(2)
    return grouped

def daily_trends(df):
    if df.empty:
        return pd.DataFrame(columns=["date", "selected_option", "votes"])
    temp = df.copy()
    temp["date"] = pd.to_datetime(temp["response_date"]).dt.date
    return temp.groupby(["date", "selected_option"]).size().reset_index(name="votes")
