"""Data validation and quality report generator for UK Top 50 dataset."""

from pathlib import Path
import re
import pandas as pd
from typing import Dict, Any

from src.load import load_raw_data, clean_data, PROJECT_ROOT

DATA_QUALITY_DOC = PROJECT_ROOT / "docs" / "data_quality.md"
ARTIST_DELIMITER_DOC = PROJECT_ROOT / "docs" / "artist_delimiter_review.md"


def run_validation_checks(raw_df: pd.DataFrame) -> Dict[str, Any]:
    """Perform comprehensive data quality checks on the raw dataset."""
    results = {}

    # Basic shape
    results["total_rows"] = len(raw_df)
    results["total_columns"] = len(raw_df.columns)
    results["columns"] = list(raw_df.columns)

    # Date analysis
    date_col = pd.to_datetime(raw_df["date"], dayfirst=True)
    results["min_date"] = date_col.min().strftime("%Y-%m-%d")
    results["max_date"] = date_col.max().strftime("%Y-%m-%d")
    results["total_unique_dates"] = date_col.nunique()

    # Full date sequence check
    full_date_range = pd.date_range(start=date_col.min(), end=date_col.max(), freq="D")
    missing_dates = full_date_range.difference(date_col)
    results["missing_dates_count"] = len(missing_dates)
    results["missing_dates_list"] = [d.strftime("%Y-%m-%d") for d in missing_dates]

    # Row count per date check (expected 50 per day)
    date_counts = date_col.value_counts()
    anomalous_dates = date_counts[date_counts != 50]
    results["anomalous_dates_count"] = len(anomalous_dates)
    results["anomalous_dates"] = anomalous_dates.to_dict()

    # Duplicate (date, position) check
    dup_mask = raw_df.duplicated(subset=["date", "position"], keep=False)
    results["duplicate_date_pos_count"] = dup_mask.sum()

    # Null value counts
    results["null_counts"] = raw_df.isnull().sum().to_dict()

    # Value sets
    results["album_type_values"] = (
        raw_df["album_type"].value_counts(dropna=False).to_dict()
    )
    results["is_explicit_values"] = (
        raw_df["is_explicit"].value_counts(dropna=False).to_dict()
    )

    # Numeric range checks
    results["position_min"] = raw_df["position"].min()
    results["position_max"] = raw_df["position"].max()
    results["popularity_min"] = raw_df["popularity"].min()
    results["popularity_max"] = raw_df["popularity"].max()
    results["total_tracks_min"] = raw_df["total_tracks"].min()
    results["total_tracks_max"] = raw_df["total_tracks"].max()
    results["duration_ms_min"] = raw_df["duration_ms"].min()
    results["duration_ms_max"] = raw_df["duration_ms"].max()

    # Duration anomaly check (< 30 seconds or > 20 minutes)
    short_tracks = raw_df[raw_df["duration_ms"] < 30000]
    long_tracks = raw_df[raw_df["duration_ms"] > 1200000]
    results["short_tracks_count"] = len(short_tracks)
    results["long_tracks_count"] = len(long_tracks)

    # Delimiter counts in raw artist strings
    artist_series = raw_df["artist"].dropna().astype(str)
    results["delimiter_counts"] = {
        "&": artist_series.str.contains(r"&", regex=True).sum(),
        ",": artist_series.str.contains(r",", regex=True).sum(),
        "feat.": artist_series.str.contains(r"feat\.?", case=False, regex=True).sum(),
        "ft.": artist_series.str.contains(r"ft\.?", case=False, regex=True).sum(),
        ";": artist_series.str.contains(r";", regex=True).sum(),
        " x ": artist_series.str.contains(r"\bx\b", case=False, regex=True).sum(),
        " with ": artist_series.str.contains(r"\bwith\b", case=False, regex=True).sum(),
    }

    return results


def generate_data_quality_report(
    results: Dict[str, Any], output_path: Path = DATA_QUALITY_DOC
) -> None:
    """Write formatted markdown data quality report."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    report = f"""# UK Top 50 Data Quality Report

## Dataset Summary
- **Total Rows (Track-Days)**: {results['total_rows']:,}
- **Total Columns**: {results['total_columns']}
- **Date Range**: {results['min_date']} to {results['max_date']} ({results['total_unique_dates']} unique snapshot days)
- **Missing Snapshot Dates**: {results['missing_dates_count']} days missing in full date sequence

## Integrity & Completeness Checks
- **Duplicate (date, position) Pairs**: {results['duplicate_date_pos_count']}
- **Dates with Row Count != 50**: {results['anomalous_dates_count']}

### Null Counts per Column
| Column | Null Count | Null % |
|---|---|---|
"""
    for col, count in results["null_counts"].items():
        pct = (count / results["total_rows"]) * 100
        report += f"| `{col}` | {count} | {pct:.2f}% |\n"

    report += f"""
## Column Value Sets & Distribution Ranges

### Categorical Fields
- **`album_type` Breakdown**: {results['album_type_values']}
- **`is_explicit` Raw Values**: {results['is_explicit_values']}

### Numeric Field Ranges
- **`position` Range**: {results['position_min']} to {results['position_max']}
- **`popularity` Range**: {results['popularity_min']} to {results['popularity_max']}
- **`total_tracks` Range**: {results['total_tracks_min']} to {results['total_tracks_max']}
- **`duration_ms` Range**: {results['duration_ms_min']:,} ms ({results['duration_ms_min']/60000:.2f} min) to {results['duration_ms_max']:,} ms ({results['duration_ms_max']/60000:.2f} min)
- **Duration Outliers**: {results['short_tracks_count']} tracks under 30s; {results['long_tracks_count']} tracks over 20 min.

## Artist Delimiter Frequency
Frequency of delimiter occurrences in raw `artist` strings:
| Delimiter | Occurrences |
|---|---|
"""
    for delim, count in results["delimiter_counts"].items():
        report += f"| `{delim}` | {count:,} |\n"

    report += "\n---\n*Report generated automatically by `src/validate.py`.*\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)


def generate_artist_delimiter_review(
    raw_df: pd.DataFrame, output_path: Path = ARTIST_DELIMITER_DOC
) -> None:
    """Generate review file of top artist strings containing '&' or ',' to audit band names."""
    artist_series = raw_df["artist"].dropna().astype(str)
    delimited = artist_series[artist_series.str.contains(r"&|,", regex=True)]
    top_30 = delimited.value_counts().head(30)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = """# Top 30 Delimited Artist Strings Review

Review of the 30 most frequent raw artist strings containing `&` or `,`:

| Raw Artist String | Track-Day Count | Recommended Action / Exception Status |
|---|---|---|
"""
    from src.artist_exceptions import is_band_exception

    for artist_str, count in top_30.items():
        is_exc = is_band_exception(artist_str)
        status = "Band Exception (Keep intact)" if is_exc else "Collaboration (Split)"
        content += f"| `{artist_str}` | {count:,} | {status} |\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    raw_df = load_raw_data()
    results = run_validation_checks(raw_df)
    generate_data_quality_report(results)
    generate_artist_delimiter_review(raw_df)
    clean_data(raw_df)  # verify cleaning runs without error
    print("Data validation successfully completed.")
    print(f"Data quality report saved to: {DATA_QUALITY_DOC}")
    print(f"Artist delimiter review saved to: {ARTIST_DELIMITER_DOC}")


if __name__ == "__main__":
    main()
