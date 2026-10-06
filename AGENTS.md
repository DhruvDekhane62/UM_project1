# UK Top 50 Playlist Analysis (Unified Mentor Project One)

## Purpose
Analyse a daily UK Top 50 playlist dataset for the client, Atlantic Recording Corporation. The focus is market structure: artist diversity and dominance, collaboration, explicit content, release format (single vs album) and track duration. This is not a popularity-prediction project.

## Deliverables
1. Research paper (EDA, insights, recommendations): `paper/paper.md`, exported later to the format the user confirms.
2. Streamlit dashboard with live analytics: `app.py`.
3. One-page executive summary: `paper/executive_summary.md`.

## The five client questions (everything traces back to these)
1. How is artist dominance distributed in the UK market?
2. Do UK charts favour domestic or international artists? (needs country data, see `/enrich-country`)
3. How do collaborations influence chart presence?
4. Does explicit content perform differently in the UK? (UK-only data: describe, do not claim a UK vs US difference)
5. How does album structure (single vs album size) relate to chart success? (only charting tracks are in the data: describe, do not claim causation)

The decisions the client wants to inform: artist signing strategy, UK-specific marketing, release format optimisation, cross-border promotion planning.

## Dataset
Location: `data/raw/uk_top50.csv` (read-only). Columns are described in `docs/data_dictionary.md`. Expected shape: 50 rows per date, `position` from 1 to 50.
Fields: date, position, song, artist, popularity, duration_ms, album_type, total_tracks, is_explicit, album_cover_url.

## Stack
Python 3.11+, pandas, numpy, plotly, streamlit, networkx, pyvis, pytest, black. Python first; no other languages unless I ask.

## Folder layout
```
app.py                 Streamlit entry point (layout only, no calculations)
src/load.py            read, validate, clean, split artists
src/metrics.py         every KPI and table, pure functions
src/charts.py          Plotly figure builders
src/validate.py        data quality report generator
tests/                 pytest tests using tiny hand-made fixtures
data/raw/              original CSV, never edited
data/external/         cached lookups (artist country)
data/processed/        cleaned data used by the app
outputs/tables/        every number in the paper comes from here
outputs/figures/       figures used in the paper
docs/                  data dictionary, decisions log, open questions, data quality report
paper/                 paper and executive summary
```

## Commands
- Validate data: `python -m src.validate`
- Tests: `pytest -q`
- Format: `black .`
- Run the app: `streamlit run app.py`

## Working agreements
- Read every file in `.agents/rules/` before writing code.
- Plan first, then code. Stop for my approval after each phase: validation, metrics, dashboard, paper.
- Slash commands available: `/validate-data`, `/build-metrics`, `/enrich-country`, `/build-dashboard`, `/draft-paper`, `/final-qa`.
- Never invent numbers. If something is missing or ambiguous, add it to `docs/open_questions.md` and ask me.
- Append every non-obvious choice to `docs/decisions.md` (date, decision, reason).
- Keep changes small and explain them in plain language; I need to be able to explain every number to my mentor.
