"""Tests for metrics and KPI functions in src/metrics.py."""

import pandas as pd
import pytest
from src.metrics import (
    calculate_summary_kpis,
    filter_dataset,
    get_top_artists_leaderboard,
)


@pytest.fixture
def sample_cleaned_df():
    return pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-05-18", "2024-05-18", "2024-05-19"]),
            "position": [1, 2, 3],
            "song": ["Song A", "Song B", "Song C"],
            "artist": ["Artist One", "Artist Two & Artist Three", "Artist One"],
            "artist_list": [
                ["Artist One"],
                ["Artist Two", "Artist Three"],
                ["Artist One"],
            ],
            "n_artists": [1, 2, 1],
            "is_collab": [False, True, False],
            "popularity": [90, 80, 85],
            "duration_ms": [180000, 200000, 210000],
            "duration_min": [3.0, 3.33, 3.5],
            "dur_bucket": ["2:30-3:30", "2:30-3:30", "3:30-4:30"],
            "album_type": ["single", "album", "single"],
            "total_tracks": [1, 12, 1],
            "is_explicit": [False, True, False],
            "rank_group": ["Top 10", "Top 10", "Top 10"],
        }
    )


def test_calculate_summary_kpis(sample_cleaned_df):
    kpis = calculate_summary_kpis(sample_cleaned_df)

    assert kpis["total_track_days"] == 3
    assert kpis["unique_artists"] == 3
    assert kpis["total_credits"] == 4
    assert kpis["collab_ratio"] == pytest.approx(33.333, rel=1e-2)
    assert kpis["explicit_share"] == pytest.approx(33.333, rel=1e-2)
    assert kpis["single_share"] == pytest.approx(66.666, rel=1e-2)


def test_filter_dataset(sample_cleaned_df):
    # Filter by collab
    collab_only = filter_dataset(sample_cleaned_df, collab_option="Collaborations Only")
    assert len(collab_only) == 1
    assert collab_only.iloc[0]["song"] == "Song B"

    # Filter by artist
    artist_filtered = filter_dataset(sample_cleaned_df, selected_artists=["Artist Two"])
    assert len(artist_filtered) == 1
    assert artist_filtered.iloc[0]["song"] == "Song B"


def test_top_artists_leaderboard(sample_cleaned_df):
    leaderboard = get_top_artists_leaderboard(sample_cleaned_df, top_n=5)
    assert len(leaderboard) == 3
    assert leaderboard.iloc[0]["Artist"] == "Artist One"
    assert leaderboard.iloc[0]["Total Credits"] == 2
