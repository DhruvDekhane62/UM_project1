---
description: Load the raw UK Top 50 CSV, validate it and write a data quality report
---
1. Confirm `data/raw/uk_top50.csv` exists. If it does not, stop and ask me to download it using the Dataset link on the last page of the brief.
2. Read `docs/data_dictionary.md` and `.agents/rules/data-integrity.md`.
3. Write `src/load.py` (loading and cleaning) and `src/validate.py` (report generator). The report must cover: shape, date range, days missing from the range, dates with a row count other than 50, duplicate (date, position) rows, nulls per column, value sets for `album_type` and `is_explicit`, range of `popularity`, `position`, `total_tracks`, and `duration_ms` (flag tracks under 30 seconds or over 20 minutes), and which artist delimiters occur (`&`, `,`, `feat.`, `;`, `x`) with counts.
// turbo
4. Run `python -m src.validate` to write `docs/data_quality.md`.
5. From the report, list the 30 most frequent artist strings that contain `&` or `,` so we can decide which are band names. Save them to `docs/artist_delimiter_review.md`.
6. Summarise for me in plain language: what is clean, what is wrong, what you propose to do about each problem. Do not fix anything yet.
7. Stop and wait for my approval before starting `/build-metrics`.
