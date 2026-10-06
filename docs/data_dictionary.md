# Data dictionary (from the project brief; verify against the real file)

| Column | Description in the brief | Verify |
|---|---|---|
| date | Date of playlist snapshot | Parses as a date; range and gaps |
| position | Playlist rank (1 to 50) | Integer 1 to 50, unique per date |
| song | Song title | Nulls, duplicates across dates are expected |
| artist | Artist(s) | Which delimiters separate collaborations |
| popularity | "Popularity score from Atlantic API" | Actual range (assumed 0 to 100) |
| duration_ms | Song duration in milliseconds | Outliers under 30 s or over 20 min |
| album_type | Single / Album | Full set of values (for example compilation) |
| total_tracks | Number of tracks in album | Integer at least 1; how EPs are labelled |
| is_explicit | Explicit content flag | Stored as boolean or as the strings "True" and "False" |
| album_cover_url | Album artwork URL | Not needed for analysis |

## Notes
- The brief calls the dataset a daily UK Top 50 playlist. Date coverage is not stated.
- The same song appears on many dates, so chart presence is counted in track-days.
