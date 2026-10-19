"""Matplotlib/Seaborn exports and Plotly interactive figures."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from src.poll_analysis import vote_share, segment_analysis, daily_trends

def save_charts(df, output_dir="outputs/charts"):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    if df.empty:
        return []
    shares = vote_share(df)
    paths = []
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=shares, x="option", y="votes", hue="option", dodge=False, legend=False, ax=ax)
    ax.set(title="Option-wise votes", xlabel="Option", ylabel="Votes")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    p = out / "overall_results.png"
    fig.savefig(p, dpi=150); plt.close(fig); paths.append(p)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(shares["votes"], labels=shares["option"], autopct="%1.1f%%")
    ax.set_title("Vote share")
    p = out / "response_distribution.png"
    fig.savefig(p, dpi=150, bbox_inches="tight"); plt.close(fig); paths.append(p)

    region = segment_analysis(df, "region")
    pivot = region.pivot(index="region", columns="selected_option", values="percentage").fillna(0)
    ax = pivot.plot(kind="bar", stacked=True, figsize=(10, 6))
    ax.set(title="Within-region vote share (%)", ylabel="Percent", xlabel="Region")
    ax.legend(title="Option", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig = ax.get_figure(); fig.tight_layout()
    p = out / "region_stacked.png"
    fig.savefig(p, dpi=150, bbox_inches="tight"); plt.close(fig); paths.append(p)

    trend = daily_trends(df)
    pivot = trend.pivot(index="date", columns="selected_option", values="votes").fillna(0)
    ax = pivot.plot(figsize=(10, 5))
    ax.set(title="Daily response counts", xlabel="Date", ylabel="Votes")
    fig = ax.get_figure(); fig.tight_layout()
    p = out / "response_trends.png"
    fig.savefig(p, dpi=150); plt.close(fig); paths.append(p)
    return paths

def interactive_bar(df):
    shares = vote_share(df)
    return px.bar(shares, x="option", y="votes", color="option",
                  hover_data=["percentage"], title="Option-wise votes")

def interactive_region(df):
    reg = segment_analysis(df, "region")
    return px.bar(reg, x="region", y="percentage", color="selected_option",
                  barmode="stack", title="Response share within each region")

def interactive_trend(df):
    return px.line(daily_trends(df), x="date", y="votes",
                   color="selected_option", markers=True, title="Daily responses")
