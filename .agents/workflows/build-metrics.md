---
description: Implement cleaning, artist splitting, KPIs and analysis tables with tests
---
1. Read `.agents/rules/kpi-definitions.md`, `python-style.md` and `docs/decisions.md`. Apply the cleaning decisions I approved after validation.
2. Extend `src/load.py`: parse types, split artists (exception list in `src/artist_exceptions.py`), add `artist_list`, `n_artists`, `is_collab`, `duration_min`, and write `data/processed/uk_top50_clean.parquet`.
3. Write `src/metrics.py` with one function per KPI and one per analysis table: artist appearances, daily concentration metrics, collaboration by rank group, mean position solo vs collaboration, explicit share by rank group, popularity and position by explicit flag, album type share, `total_tracks` distribution, duration buckets against popularity, collaboration network edges.
4. Write `tests/test_metrics.py` with a tiny hand-made fixture whose answers you calculate by hand in comments.
// turbo
5. Run `pytest -q` and fix failures. Do not weaken a test to make it pass; tell me if a test exposes an ambiguity in a definition.
6. Write every table to `outputs/tables/` as CSV, including `kpis_overall.csv` for the full date range.
7. Run the `kpi-audit` skill and show me its result table.
8. Summarise the headline numbers and any surprising results. Stop and wait for my approval.
