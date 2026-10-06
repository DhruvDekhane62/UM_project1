"""Tests for data loading and preprocessing routines in src/load.py."""

import pandas as pd
import pytest
from src.load import (
    split_artist_string,
    parse_explicit_column,
    assign_duration_bucket,
    clean_data,
)


def test_split_artist_string_band_exceptions():
    # Known band exceptions should NOT be split
    assert split_artist_string("Florence + The Machine") == ["Florence + The Machine"]
    assert split_artist_string("Mumford & Sons") == ["Mumford & Sons"]
    assert split_artist_string("Bob Marley & The Wailers") == [
        "Bob Marley & The Wailers"
    ]


def test_split_artist_string_collaborations():
    # Regular collaborations should be split
    assert split_artist_string("Calvin Harris & Ellie Goulding") == [
        "Calvin Harris",
        "Ellie Goulding",
    ]
    assert split_artist_string("David Guetta feat. Bebe Rexha") == [
        "David Guetta",
        "Bebe Rexha",
    ]
    assert split_artist_string("Central Cee ft. LIL BABY") == [
        "Central Cee",
        "LIL BABY",
    ]
    assert split_artist_string("PinkPantheress & Ice Spice") == [
        "PinkPantheress",
        "Ice Spice",
    ]


def test_parse_explicit_column():
    s = pd.Series(["TRUE", "False", "1", "0", "true", "false", True, False])
    parsed = parse_explicit_column(s)
    expected = pd.Series([True, False, True, False, True, False, True, False])
    pd.testing.assert_series_equal(parsed, expected)


def test_assign_duration_bucket():
    assert assign_duration_bucket(2.1) == "<2:30"
    assert assign_duration_bucket(3.0) == "2:30-3:30"
    assert assign_duration_bucket(4.0) == "3:30-4:30"
    assert assign_duration_bucket(5.2) == ">=4:30"


def test_clean_data_pipeline():
    sample_raw = pd.DataFrame(
        {
            "date": ["18-05-2024", "19-05-2024"],
            "position": ["1", "2"],
            "song": ["Tattoo", "Miracle"],
            "artist": ["Loreen", "Calvin Harris & Ellie Goulding"],
            "popularity": [89, 91],
            "duration_ms": [183374, 186496],
            "album_type": ["single", "single"],
            "total_tracks": [1, 1],
            "is_explicit": ["FALSE", "FALSE"],
            "album_cover_url": ["http://example.com/1", "http://example.com/2"],
        }
    )

    cleaned = clean_data(sample_raw)
    assert len(cleaned) == 2
    assert cleaned.loc[1, "is_collab"] == True
    assert cleaned.loc[0, "is_collab"] == False
    assert len(cleaned.loc[1, "artist_list"]) == 2
