import plotly.express as px
import pandas as pd

def create_status_pie_chart(df: pd.DataFrame):
    """
    Creates an interactive Plotly donut chart showing application statuses.
    Uses transparent background so it looks great in both Dark and Light themes.
    """
    if df.empty or "status" not in [col.lower() for col in df.columns]:
        return None

    # Handle case-insensitive column name
    status_col = [col for col in df.columns if col.lower() == "status"][0]
    status_counts = df[status_col].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    color_map = {
        "Applied": "#3b82f6",     # Blue
        "Interview": "#f59e0b",   # Amber
        "Offer": "#10b981",       # Green
        "Rejected": "#ef4444",    # Red
        "Wishlist": "#8b5cf6"     # Purple
    }

    fig = px.pie(
        status_counts,
        names="Status",
        values="Count",
        hole=0.45,
        color="Status",
        color_discrete_map=color_map,
        title="Application Status Breakdown"
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hoverinfo="label+value+percent"
    )
    fig.update_layout(
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=20, l=20, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    return fig

def create_timeline_chart(df: pd.DataFrame):
    """
    Creates a timeline bar chart showing application counts by applied date.
    Uses transparent background for seamless light and dark mode integration.
    """
    date_col = None
    for col in df.columns:
        if "applied" in col.lower() or "date" in col.lower():
            date_col = col
            break

    if df.empty or not date_col:
        return None

    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors="coerce")
    df_copy = df_copy.dropna(subset=[date_col])

    if df_copy.empty:
        return None

    date_counts = df_copy.groupby(df_copy[date_col].dt.date).size().reset_index(name="Applications")
    date_counts.columns = ["Date", "Applications"]
    date_counts = date_counts.sort_values(by="Date")

    fig = px.bar(
        date_counts,
        x="Date",
        y="Applications",
        title="Applications Over Time",
        labels={"Date": "Date Applied", "Applications": "Number of Applications"},
        color_discrete_sequence=["#3b82f6"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickformat="%Y-%m-%d"),
        margin=dict(t=40, b=20, l=20, r=20)
    )
    return fig
