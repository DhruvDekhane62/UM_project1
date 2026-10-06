---
name: kpi-audit
description: Audit that KPI code, dashboard values and paper numbers all match .agents/rules/kpi-definitions.md. Use when metrics are first implemented, whenever a KPI or the artist split rule changes, before drafting the paper, and during final QA.
---

# KPI audit

## Steps
1. Read `.agents/rules/kpi-definitions.md`.
2. For each KPI, open its function in `src/metrics.py` and compare unit, denominator and formula against the definition.
3. Independently recompute every KPI for three dates chosen with `random.Random(42)`, using a different method from the implementation (for example plain Python `collections.Counter` instead of pandas `groupby`). Compare with the module output; they must agree to 1e-9.
4. Compare with the saved tables in `outputs/tables/` and with the dashboard KPI row at the full date range.
5. Search `paper/paper.md` and `paper/executive_summary.md` for numbers and confirm each one traces to a table.

## Output
A table with one row per KPI and the columns: definition matches, code matches, independent recompute matches, dashboard matches, paper matches. List mismatches first, with the values that disagree. Do not fix anything silently; propose the fix and wait for approval.
