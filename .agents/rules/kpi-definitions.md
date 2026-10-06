# KPI definitions (single source of truth)

The brief names these KPIs but does not define them, so these are my defaults. If a definition changes, update this file, `tests/`, the app and the paper appendix together, and log it in `docs/decisions.md`.

## Units
- **Track-day**: one row of the cleaned data (a song in a position on a date). Chart presence is measured in track-days.
- **Credit**: one artist on one track-day after splitting collaborations. A solo track-day has one credit; a three-artist collaboration has three.
- **Unique song**: a distinct (song, artist) pair. Used for the collaboration network and catalogue-breadth checks.

## Definitions
| KPI | Definition | Formula |
|---|---|---|
| Unique Artist Count | Distinct artists per day after splitting | `nunique(artist_name)` per date |
| Diversity score | Unique artists divided by credits that day (stays between 0 and 1) | `unique / credits` |
| Playlist concentration ratio | Share of credits held by the 5 most frequent artists | `top5 credits / all credits` |
| Artist Concentration Index | Herfindahl-Hirschman Index over artist credit shares | `sum(share^2)` |
| Content Variety Index | Normalised Shannon entropy of artist credit shares | `-sum(p ln p) / ln(n)`, 0 when n = 1 |
| Collaboration Ratio | Share of track-days with two or more credited artists | `mean(n_artists > 1)` |
| Explicit Content Share | Share of track-days flagged explicit | `mean(is_explicit)` |
| Single vs Album Ratio | Share of track-days by `album_type` | `value_counts(normalize=True)` |

## Groupings
- Rank groups: Top 10 = positions 1 to 10, Rest = positions 11 to 50, and Top 50 overall.
- Duration buckets in minutes: under 2:30, 2:30 to 3:30, 3:30 to 4:30, 4:30 and over.
- Popularity buckets: quartiles with `pd.qcut(..., duplicates="drop")`.

## Reporting rules
- Daily KPIs are computed per date and then summarised (mean, min, max). Period KPIs are computed on all credits in the selected window. Always label which one is shown.
- Show ratios as percentages and keep the denominator available in a table or tooltip.
- Do not compute KPIs in `app.py`; call the functions in `src/metrics.py`.
