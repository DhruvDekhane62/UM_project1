---
description: Final consistency, reproducibility and submission check before handing in
---
1. Run the `kpi-audit` skill and show me the result table.
// turbo
2. Run `black --check .` and `pytest -q`.
3. Reproduce from scratch: delete `data/processed/` and `outputs/`, rerun the pipeline, and confirm the same numbers appear. Report any difference.
4. Check that every number in `paper/paper.md` and `paper/executive_summary.md` appears in a table in `outputs/tables/` with the same value and rounding.
5. Check that `requirements.txt` has pinned versions and that a fresh virtual environment can run the app.
6. Check the README: purpose, setup, how to run, folder map, how KPIs are defined, known limitations.
7. Produce a submission checklist: paper exported in the required format, dashboard link tested in a private browser window, repository link, executive summary, anything still open in `docs/open_questions.md`.
