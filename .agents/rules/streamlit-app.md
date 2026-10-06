# Streamlit app rules

## Structure
- `app.py` only lays out widgets and calls `src/metrics.py` and `src/charts.py`.
- Wrap data loading in `st.cache_data`. The app must start from `data/processed/` and must not need `data/raw/`.

## Required modules (tabs)
1. Artists: dominance leaderboard (top 15), daily unique-artist trend.
2. Collaborations: solo vs collaboration split, by rank group, network graph.
3. Explicit content: share overall and by rank group, popularity by flag.
4. Album types: single vs album split, `total_tracks` distribution.
5. Duration: duration histogram, popularity by duration bucket.

## Required filters (sidebar)
Date range, artist, solo vs collaboration toggle, album type. All filters feed one `apply_filters()` function.

## Behaviour to get right
- A KPI row at the top: unique artists, collaboration ratio, explicit share, single share, top 5 artist share.
- Half-selected date range (only one date picked): stop quietly until both dates exist.
- Filters that return no rows: show a plain message that says what to change ("Widen the date range or clear the artist filter") and stop.
- Artist filter keeps a track if any credited artist is selected.
- Check the installed Streamlit version before using chart width arguments; some arguments are deprecated in newer versions.
- Use a colour-blind-safe palette and label axes with units. Chart titles describe the chart; takeaways belong in the paper.
- Network graph: nodes sized by appearances, edges weighted by number of shared unique songs, capped to the top artists so it stays readable.

## Deployment
- Pin versions in `requirements.txt` after the first successful run.
- Keep the processed data small enough for a GitHub repo (under 100 MB per file; prefer parquet). Ask me before publishing any data.
- Test the app in the browser tool: every filter alone, every filter together, and an empty result.
