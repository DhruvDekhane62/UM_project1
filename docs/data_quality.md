# UK Top 50 Data Quality Report

## Dataset Summary
- **Total Rows (Track-Days)**: 27,800
- **Total Columns**: 10
- **Date Range**: 2024-05-18 to 2025-11-27 (555 unique snapshot days)
- **Missing Snapshot Dates**: 4 days missing in full date sequence

## Integrity & Completeness Checks
- **Duplicate (date, position) Pairs**: 100
- **Dates with Row Count != 50**: 1

### Null Counts per Column
| Column | Null Count | Null % |
|---|---|---|
| `date` | 0 | 0.00% |
| `position` | 0 | 0.00% |
| `song` | 0 | 0.00% |
| `artist` | 0 | 0.00% |
| `popularity` | 0 | 0.00% |
| `duration_ms` | 0 | 0.00% |
| `album_type` | 0 | 0.00% |
| `total_tracks` | 0 | 0.00% |
| `is_explicit` | 0 | 0.00% |
| `album_cover_url` | 0 | 0.00% |

## Column Value Sets & Distribution Ranges

### Categorical Fields
- **`album_type` Breakdown**: {'album': 16669, 'single': 11053, 'compilation': 78}
- **`is_explicit` Raw Values**: {False: 18888, True: 8912}

### Numeric Field Ranges
- **`position` Range**: 1 to 50
- **`popularity` Range**: 0 to 100
- **`total_tracks` Range**: 1 to 119
- **`duration_ms` Range**: 37,314 ms (0.62 min) to 587,364 ms (9.79 min)
- **Duration Outliers**: 0 tracks under 30s; 0 tracks over 20 min.

## Artist Delimiter Frequency
Frequency of delimiter occurrences in raw `artist` strings:
| Delimiter | Occurrences |
|---|---|
| `&` | 5,124 |
| `,` | 196 |
| `feat.` | 0 |
| `ft.` | 2,134 |
| `;` | 0 |
| ` x ` | 0 |
| ` with ` | 0 |

---
*Report generated automatically by `src/validate.py`.*
