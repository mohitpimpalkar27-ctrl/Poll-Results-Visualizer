"""Rule-based descriptive insights; no statistical inference or AI claims."""
from src.poll_analysis import vote_share

def generate_insights(df):
    if df.empty:
        return ["No valid responses for the selected filters."]
    shares = vote_share(df)
    top = shares.iloc[0]
    n = len(df)
    result = [
        f"Analyzed {n:,} valid responses from {df['respondent_id'].nunique():,} unique respondents.",
        f"Leading option: {top['option']} with {int(top['votes']):,} votes ({top['percentage']:.2f}%).",
    ]
    if len(shares) > 1:
        second = shares.iloc[1]
        lead = float(top["percentage"] - second["percentage"])
        result.append(f"Lead over {second['option']}: {lead:.2f} percentage points.")
    result.append("These are descriptive results for the selected sample, not population estimates.")
    return result
