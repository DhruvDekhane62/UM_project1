"""Data loading, cleaning, artist splitting, and preprocessing module for UK Top 50 Playlist."""

from pathlib import Path
import re
import pandas as pd
from typing import List, Set, Union
from src.artist_exceptions import is_band_exception
from src.metrics import explode_artist_credits  # re-export for convenience

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "uk_top50.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "uk_top50_cleaned.parquet"


def split_artist_string(artist_str: str) -> List[str]:
    """Split an artist string into individual credited artist names, preserving known band names.

    Delimiters handled: '&', 'feat.', 'ft.', ',', ' x ', ' with ' (case insensitive).
    """
    if not isinstance(artist_str, str) or not artist_str.strip():
        return ["Unknown"]

    clean_str = artist_str.strip()
    if is_band_exception(clean_str):
        return [clean_str]

    # Pattern for splitting multi-artist strings
    # Splits on &, feat., ft., with, x, and comma (when not inside band names)
    pattern = r"\s*(?:&|feat\.?|ft\.?|with|(?<=\s)x(?=\s)|,)\s*"

    # Pre-clean string for regex matching
    raw_splits = re.split(pattern, clean_str, flags=re.IGNORECASE)

    artists = [a.strip() for a in raw_splits if a and a.strip()]
    return artists if artists else [clean_str]


def parse_explicit_column(series: pd.Series) -> pd.Series:
    """Explicitly parse is_explicit column into boolean values to handle string representations safely."""
    if series.dtype == bool:
        return series

    str_series = series.astype(str).str.strip().str.lower()
    return str_series.isin(["true", "1", "t", "yes"])


def assign_duration_bucket(duration_min: float) -> str:
    """Categorize duration in minutes into predefined buckets."""
    if pd.isna(duration_min):
        return "Unknown"
    if duration_min < 2.5:
        return "<2:30"
    elif duration_min < 3.5:
        return "2:30-3:30"
    elif duration_min < 4.5:
        return "3:30-4:30"
    else:
        return ">=4:30"


def load_raw_data(csv_path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load raw UK Top 50 CSV dataset without modifications."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Raw data file not found at: {csv_path}")
    return pd.read_csv(csv_path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean, validate, and enrich raw UK Top 50 DataFrame."""
    cleaned = df.copy()

    # Standardize column names to snake_case
    cleaned.columns = [col.strip().lower() for col in cleaned.columns]

    # Date parsing
    cleaned["date"] = pd.to_datetime(cleaned["date"], dayfirst=True)

    # Numeric columns
    cleaned["position"] = pd.to_numeric(cleaned["position"], errors="coerce").astype(
        int
    )
    cleaned["popularity"] = pd.to_numeric(cleaned["popularity"], errors="coerce")
    cleaned["duration_ms"] = pd.to_numeric(cleaned["duration_ms"], errors="coerce")
    cleaned["total_tracks"] = (
        pd.to_numeric(cleaned["total_tracks"], errors="coerce").fillna(1).astype(int)
    )

    # Duration in minutes & buckets
    cleaned["duration_min"] = cleaned["duration_ms"] / 60000.0
    cleaned["dur_bucket"] = cleaned["duration_min"].apply(assign_duration_bucket)

    # Boolean explicitness
    cleaned["is_explicit"] = parse_explicit_column(cleaned["is_explicit"])

    # Album type normalization
    cleaned["album_type"] = cleaned["album_type"].astype(str).str.strip().str.lower()

    # Artist splitting
    cleaned["artist_list"] = cleaned["artist"].apply(split_artist_string)
    cleaned["n_artists"] = cleaned["artist_list"].apply(len)
    cleaned["is_collab"] = cleaned["n_artists"] > 1

    # Rank groups
    cleaned["rank_group"] = cleaned["position"].apply(
        lambda pos: "Top 10" if pos <= 10 else "Rest 11-50"
    )

    return cleaned


def get_processed_data(force_reprocess: bool = False) -> pd.DataFrame:
    """Get cleaned data, loading from parquet cache if available."""
    if PROCESSED_DATA_PATH.exists() and not force_reprocess:
        return pd.read_parquet(PROCESSED_DATA_PATH)

    raw_df = load_raw_data()
    cleaned_df = clean_data(raw_df)

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_parquet(PROCESSED_DATA_PATH, index=False)
    return cleaned_df


if __name__ == "__main__":
    df = get_processed_data(force_reprocess=True)
    print(f"Processed dataset saved successfully. Shape: {df.shape}")
