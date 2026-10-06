# Python style

- Follow PEP 8 and format with `black`. Use type hints on every function in `src/`.
- Prefer pure functions that take a DataFrame and return a DataFrame or a dict. No hidden global state, no computation at import time.
- Use vectorised pandas operations; avoid row-by-row loops unless building the network graph.
- Name columns in snake_case exactly as the dataset does. Derived columns: `artist_list`, `n_artists`, `is_collab`, `duration_min`, `rank_group`, `dur_bucket`.
- Every KPI function has a docstring stating its definition and denominator, matching `kpi-definitions.md`.
- Tests live in `tests/` and use a tiny hand-made DataFrame (about 3 dates, 6 to 10 rows) whose correct answers you can verify by hand. Include a case for a band name that contains "&", a collaboration with three artists, and a day with fewer than 50 rows.
- Random or sampled operations use `seed=42`.
- Use `pathlib.Path` for paths relative to the project root so the app also runs after deployment.
- Do not add a dependency without adding it to `requirements.txt` and telling me why.
