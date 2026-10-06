"""Pure metrics and KPI calculation functions for UK Top 50 dataset."""

import math
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd


def filter_dataset(
    df: pd.DataFrame,
    start_date: Optional[pd.Timestamp] = None,
    end_date: Optional[pd.Timestamp] = None,
    selected_artists: Optional[List[str]] = None,
    collab_option: str = "All",
    selected_album_types: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Filter dataset based on sidebar options."""
    filtered = df.copy()

    if start_date is not None and end_date is not None:
        filtered = filtered[
            (filtered["date"] >= start_date) & (filtered["date"] <= end_date)
        ]

    if selected_album_types and len(selected_album_types) > 0:
        filtered = filtered[filtered["album_type"].isin(selected_album_types)]

    if collab_option == "Solo Only":
        filtered = filtered[~filtered["is_collab"]]
    elif collab_option == "Collaborations Only":
        filtered = filtered[filtered["is_collab"]]

    if selected_artists and len(selected_artists) > 0:
        artist_set = set(selected_artists)
        filtered = filtered[
            filtered["artist_list"].apply(
                lambda artists: bool(set(artists) & artist_set)
            )
        ]

    return filtered


def explode_artist_credits(df: pd.DataFrame) -> pd.DataFrame:
    """Explode track-day dataframe so each credited artist is one row (credit)."""
    if df.empty:
        return pd.DataFrame(columns=list(df.columns) + ["artist_name"])

    exploded = df.explode("artist_list").rename(columns={"artist_list": "artist_name"})
    exploded["artist_name"] = exploded["artist_name"].str.strip()
    return exploded


def calculate_summary_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate summary KPIs for the current dataset slice."""
    if df.empty:
        return {
            "total_track_days": 0,
            "unique_songs": 0,
            "unique_artists": 0,
            "total_credits": 0,
            "collab_ratio": 0.0,
            "explicit_share": 0.0,
            "single_share": 0.0,
            "top5_artist_share": 0.0,
            "hhi_index": 0.0,
            "shannon_entropy": 0.0,
        }

    total_track_days = len(df)
    credits_df = explode_artist_credits(df)
    total_credits = len(credits_df)
    unique_artists = credits_df["artist_name"].nunique()

    # Unique songs as (song, artist) tuple
    unique_songs = df.groupby(["song", "artist"]).ngroups

    # Collab share
    collab_ratio = (
        (df["is_collab"].sum() / total_track_days) * 100.0
        if total_track_days > 0
        else 0.0
    )

    # Explicit share
    explicit_share = (
        (df["is_explicit"].sum() / total_track_days) * 100.0
        if total_track_days > 0
        else 0.0
    )

    # Single share
    single_count = (df["album_type"] == "single").sum()
    single_share = (
        (single_count / total_track_days) * 100.0 if total_track_days > 0 else 0.0
    )

    # Artist credits distribution
    artist_counts = credits_df["artist_name"].value_counts()
    top5_credits = artist_counts.head(5).sum()
    top5_artist_share = (
        (top5_credits / total_credits) * 100.0 if total_credits > 0 else 0.0
    )

    # HHI (Herfindahl-Hirschman Index) & Shannon Entropy
    if total_credits > 0:
        shares = artist_counts / total_credits
        hhi_index = (shares**2).sum()

        # Shannon entropy normalized: -sum(p * ln(p)) / ln(N)
        p = shares[shares > 0]
        raw_entropy = -(p * np.log(p)).sum()
        max_entropy = np.log(unique_artists) if unique_artists > 1 else 1.0
        shannon_entropy = raw_entropy / max_entropy if unique_artists > 1 else 0.0
    else:
        hhi_index = 0.0
        shannon_entropy = 0.0

    return {
        "total_track_days": total_track_days,
        "unique_songs": unique_songs,
        "unique_artists": unique_artists,
        "total_credits": total_credits,
        "collab_ratio": collab_ratio,
        "explicit_share": explicit_share,
        "single_share": single_share,
        "top5_artist_share": top5_artist_share,
        "hhi_index": hhi_index,
        "shannon_entropy": shannon_entropy,
    }


def get_top_artists_leaderboard(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Get top N artists by total credits, track-days, and unique songs."""
    if df.empty:
        return pd.DataFrame(
            columns=[
                "Artist",
                "Total Credits",
                "Track-Days",
                "Unique Songs",
                "Share (%)",
            ]
        )

    credits_df = explode_artist_credits(df)
    total_credits = len(credits_df)

    stats = (
        credits_df.groupby("artist_name")
        .agg(
            total_credits=("artist_name", "count"),
            track_days=("date", "count"),
            unique_songs=("song", "nunique"),
        )
        .reset_index()
    )

    stats["share_pct"] = (
        (stats["total_credits"] / total_credits) * 100.0 if total_credits > 0 else 0.0
    )
    stats = stats.sort_values(by="total_credits", ascending=False).head(top_n)
    stats.columns = [
        "Artist",
        "Total Credits",
        "Track-Days",
        "Unique Songs",
        "Share (%)",
    ]
    return stats


def get_daily_unique_artists(df: pd.DataFrame) -> pd.DataFrame:
    """Compute daily unique artists count and diversity score."""
    if df.empty:
        return pd.DataFrame(
            columns=["date", "unique_artists", "total_credits", "diversity_score"]
        )

    credits_df = explode_artist_credits(df)
    daily = (
        credits_df.groupby("date")
        .agg(
            unique_artists=("artist_name", "nunique"),
            total_credits=("artist_name", "count"),
        )
        .reset_index()
    )
    daily["diversity_score"] = daily["unique_artists"] / daily["total_credits"]
    return daily.sort_values(by="date")


def get_collab_breakdown_by_rank(df: pd.DataFrame) -> pd.DataFrame:
    """Compute collaboration ratio split by rank group (Top 10 vs Rest 11-50)."""
    if df.empty:
        return pd.DataFrame(
            columns=["rank_group", "total_tracks", "collab_tracks", "collab_pct"]
        )

    grouped = (
        df.groupby("rank_group")
        .agg(
            total_tracks=("position", "count"),
            collab_tracks=("is_collab", "sum"),
        )
        .reset_index()
    )
    grouped["collab_pct"] = (grouped["collab_tracks"] / grouped["total_tracks"]) * 100.0
    return grouped


def get_explicit_breakdown(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Compute explicit content breakdown overall and by rank group, plus popularity stats."""
    if df.empty:
        rank_df = pd.DataFrame(
            columns=["rank_group", "total", "explicit_count", "explicit_pct"]
        )
        pop_df = pd.DataFrame(
            columns=["is_explicit", "mean_popularity", "median_popularity", "count"]
        )
        return rank_df, pop_df

    rank_df = (
        df.groupby("rank_group")
        .agg(
            total=("position", "count"),
            explicit_count=("is_explicit", "sum"),
        )
        .reset_index()
    )
    rank_df["explicit_pct"] = (rank_df["explicit_count"] / rank_df["total"]) * 100.0

    pop_df = (
        df.groupby("is_explicit")
        .agg(
            mean_popularity=("popularity", "mean"),
            median_popularity=("popularity", "median"),
            count=("popularity", "count"),
        )
        .reset_index()
    )
    pop_df["Explicit Status"] = pop_df["is_explicit"].map(
        {True: "Explicit", False: "Clean"}
    )
    return rank_df, pop_df


def get_album_type_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Compute single vs album breakdown."""
    if df.empty:
        return pd.DataFrame(columns=["album_type", "count", "percentage"])

    counts = df["album_type"].value_counts().reset_index()
    counts.columns = ["album_type", "count"]
    total = counts["count"].sum()
    counts["percentage"] = (counts["count"] / total) * 100.0 if total > 0 else 0.0
    return counts


def get_duration_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Compute duration bucket counts and average popularity per bucket."""
    if df.empty:
        return pd.DataFrame(columns=["dur_bucket", "count", "mean_popularity"])

    bucket_order = ["<2:30", "2:30-3:30", "3:30-4:30", ">=4:30"]
    grouped = (
        df.groupby("dur_bucket")
        .agg(
            count=("position", "count"),
            mean_popularity=("popularity", "mean"),
        )
        .reindex(bucket_order)
        .reset_index()
        .dropna(subset=["count"])
    )
    return grouped


def get_collaboration_network_data(
    df: pd.DataFrame, top_n_artists: int = 30
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Build nodes and weighted edges for collaboration network graph.

    Nodes: artists (sized by total appearances)
    Edges: weighted by number of shared unique songs
    """
    if df.empty:
        return [], []

    # Get top N artists by appearances
    credits_df = explode_artist_credits(df)
    top_artists = set(
        credits_df["artist_name"].value_counts().head(top_n_artists).index
    )

    # Filter to collab tracks with at least 2 credited artists
    collab_df = df[df["is_collab"]].copy()

    # Calculate shared unique songs between pairs
    edge_counts: Dict[Tuple[str, str], Set[str]] = {}

    for _, row in collab_df.iterrows():
        song_key = f"{row['song']} - {row['artist']}"
        artists = sorted(list(set(row["artist_list"])))
        for i in range(len(artists)):
            for j in range(i + 1, len(artists)):
                a1, a2 = artists[i], artists[j]
                if a1 in top_artists or a2 in top_artists:
                    pair = (a1, a2)
                    if pair not in edge_counts:
                        edge_counts[pair] = set()
                    edge_counts[pair].add(song_key)

    nodes = []
    artist_counts = credits_df["artist_name"].value_counts()
    included_node_ids = set()

    for (a1, a2), songs in edge_counts.items():
        weight = len(songs)
        if weight > 0:
            included_node_ids.add(a1)
            included_node_ids.add(a2)

    for artist in included_node_ids:
        nodes.append(
            {
                "id": artist,
                "label": artist,
                "value": int(artist_counts.get(artist, 1)),
            }
        )

    edges = []
    for (a1, a2), songs in edge_counts.items():
        if len(songs) > 0:
            edges.append(
                {
                    "from": a1,
                    "to": a2,
                    "value": len(songs),
                    "title": f"{len(songs)} shared song(s)",
                }
            )

    return nodes, edges
