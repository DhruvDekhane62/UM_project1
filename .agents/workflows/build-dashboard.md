---
description: Build and browser-test the Streamlit dashboard from the metrics module
---
1. Read `.agents/rules/streamlit-app.md`. Confirm `src/metrics.py` tests pass before starting.
2. Write `src/charts.py` (Plotly builders) and `app.py`: KPI row, sidebar filters, five tabs, `apply_filters()` in `src/metrics.py`.
3. Add the country mix chart to the Artists tab only if `outputs/tables/country_mix.csv` exists.
// turbo
4. Run `streamlit run app.py --server.headless true` and open it in the browser tool.
5. Test and show screenshots for: default view, each filter alone, all filters together, a date range of one day, and a filter combination with no results. Fix anything broken.
6. Compare the KPI row at the full date range with `outputs/tables/kpis_overall.csv`. They must match exactly.
7. Write the app section of `README.md`: how to run locally and how to deploy to Streamlit Community Cloud.
8. Stop and wait for my approval.
