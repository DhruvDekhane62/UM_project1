"""Plotly figure builders and network graph renderer for UK Top 50 Streamlit dashboard."""

from typing import Dict, List, Any
import pandas as pd
import plotly.express as px
import plotly.graph_objects as gg
from pyvis.network import Network
import tempfile
import os

# Colour-blind safe & modern aesthetic palette
PRIMARY_COLOR = "#6366F1"  # Indigo
SECONDARY_COLOR = "#06B6D4"  # Cyan
ACCENT_COLOR = "#F43F5E"  # Rose
DARK_BG = "#0F172A"
LIGHT_BG = "#F8FAFC"

PX_THEME = "plotly_white"


def build_top_artists_chart(leaderboard_df: pd.DataFrame):
    """Horizontal bar chart for top artist credits."""
    if leaderboard_df.empty:
        fig = px.bar(title="No artist data available")
        return fig

    df_sorted = leaderboard_df.sort_values(by="Total Credits", ascending=True)
    fig = px.bar(
        df_sorted,
        x="Total Credits",
        y="Artist",
        orientation="h",
        text="Share (%)",
        title="Top 15 Most Credited Artists on UK Top 50",
        color="Total Credits",
        color_continuous_scale="Viridis",
        template=PX_THEME,
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(
        xaxis_title="Total Credits (Track-Days)",
        yaxis_title="",
        height=500,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def build_daily_unique_artists_chart(daily_df: pd.DataFrame):
    """Line chart showing daily unique artist count and diversity score."""
    if daily_df.empty:
        return px.line(title="No daily data available")

    fig = px.line(
        daily_df,
        x="date",
        y="unique_artists",
        title="Daily Unique Artist Count Over Time",
        labels={"date": "Date", "unique_artists": "Unique Artists"},
        template=PX_THEME,
        color_discrete_sequence=[PRIMARY_COLOR],
    )
    fig.update_traces(
        mode="lines+markers",
        hovertemplate="Date: %{x|%Y-%m-%d}<br>Unique Artists: %{y}",
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Unique Artists per Day",
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def build_collab_rank_chart(collab_df: pd.DataFrame):
    """Bar chart showing collaboration ratio by rank group."""
    if collab_df.empty:
        return px.bar(title="No rank group data available")

    fig = px.bar(
        collab_df,
        x="rank_group",
        y="collab_pct",
        color="rank_group",
        text="collab_pct",
        title="Collaboration Ratio: Top 10 vs Rest 11-50",
        labels={"rank_group": "Rank Group", "collab_pct": "Collaboration %"},
        template=PX_THEME,
        color_discrete_sequence=[PRIMARY_COLOR, SECONDARY_COLOR],
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="auto")
    fig.update_layout(
        xaxis_title="Rank Group",
        yaxis_title="Percentage of Tracks with Collaborations (%)",
        height=400,
        showlegend=False,
    )
    return fig


def build_explicit_chart(rank_explicit_df: pd.DataFrame, pop_explicit_df: pd.DataFrame):
    """Grouped chart for explicit content share and popularity comparison."""
    if rank_explicit_df.empty:
        return px.bar(title="No explicit data available"), px.bar(
            title="No data available"
        )

    fig_share = px.bar(
        rank_explicit_df,
        x="rank_group",
        y="explicit_pct",
        color="rank_group",
        text="explicit_pct",
        title="Explicit Tracks Share by Rank Group",
        labels={"rank_group": "Rank Group", "explicit_pct": "Explicit Share (%)"},
        template=PX_THEME,
        color_discrete_sequence=[ACCENT_COLOR, PRIMARY_COLOR],
    )
    fig_share.update_traces(texttemplate="%{text:.1f}%", textposition="auto")
    fig_share.update_layout(
        xaxis_title="Rank Group",
        yaxis_title="Explicit Share (%)",
        height=400,
        showlegend=False,
    )

    fig_pop = px.bar(
        pop_explicit_df,
        x="Explicit Status",
        y="mean_popularity",
        color="Explicit Status",
        text="mean_popularity",
        title="Average Spotify Popularity: Explicit vs Clean",
        labels={
            "Explicit Status": "Content Type",
            "mean_popularity": "Mean Popularity Score",
        },
        template=PX_THEME,
        color_discrete_sequence=[ACCENT_COLOR, SECONDARY_COLOR],
    )
    fig_pop.update_traces(texttemplate="%{text:.1f}", textposition="auto")
    fig_pop.update_layout(
        xaxis_title="",
        yaxis_title="Mean Popularity (0-100)",
        height=400,
        showlegend=False,
    )

    return fig_share, fig_pop


def build_album_type_chart(album_df: pd.DataFrame):
    """Pie/Donut chart for single vs album split."""
    if album_df.empty:
        return px.pie(title="No album type data available")

    fig = px.pie(
        album_df,
        names="album_type",
        values="count",
        title="Release Format Breakdown (Single vs Album)",
        hole=0.4,
        template=PX_THEME,
        color_discrete_sequence=[PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR],
    )
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(height=400)
    return fig


def build_duration_charts(df: pd.DataFrame, bucket_df: pd.DataFrame):
    """Histogram of track durations and popularity by duration bucket."""
    if df.empty:
        return px.histogram(title="No duration data"), px.bar(title="No duration data")

    fig_hist = px.histogram(
        df,
        x="duration_min",
        nbins=40,
        title="Track Duration Distribution (Minutes)",
        labels={"duration_min": "Duration (Minutes)"},
        template=PX_THEME,
        color_discrete_sequence=[PRIMARY_COLOR],
    )
    fig_hist.update_layout(
        xaxis_title="Duration (Minutes)",
        yaxis_title="Track-Day Count",
        height=400,
    )

    fig_pop = px.bar(
        bucket_df,
        x="dur_bucket",
        y="mean_popularity",
        color="dur_bucket",
        text="mean_popularity",
        title="Average Popularity by Duration Bucket",
        labels={"dur_bucket": "Duration Bucket", "mean_popularity": "Mean Popularity"},
        template=PX_THEME,
        color_discrete_sequence=[
            PRIMARY_COLOR,
            SECONDARY_COLOR,
            ACCENT_COLOR,
            "#10B981",
        ],
    )
    fig_pop.update_traces(texttemplate="%{text:.1f}", textposition="auto")
    fig_pop.update_layout(
        xaxis_title="Duration Bucket",
        yaxis_title="Mean Popularity Score",
        height=400,
        showlegend=False,
    )

    return fig_hist, fig_pop


def generate_network_html(
    nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]
) -> str:
    """Generate PyVis network graph HTML string."""
    net = Network(height="500px", width="100%", bgcolor="#0F172A", font_color="#FFFFFF")

    for n in nodes:
        net.add_node(
            n["id"],
            label=n["label"],
            title=f"{n['label']} ({n['value']} appearances)",
            value=max(n["value"], 5),
            color="#6366F1",
        )

    for e in edges:
        net.add_edge(
            e["from"],
            e["to"],
            value=e["value"],
            title=e["title"],
            color="#06B6D4",
        )

    net.toggle_physics(True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        net.save_graph(tmp.name)
        tmp_path = tmp.name

    with open(tmp_path, "r", encoding="utf-8") as f:
        html_code = f.read()

    os.remove(tmp_path)
    return html_code
