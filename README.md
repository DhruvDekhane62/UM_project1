# 🎵 United Kingdom Top 50 Playlist Market Structure, Artist Diversity & Content Localization Analysis

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dhruvdekhane62-um-project1-app-uugher.streamlit.app/)
![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Pytest Status](https://img.shields.io/badge/Tests-8%20Passed-brightgreen?style=flat&logo=pytest)
![Client](https://img.shields.io/badge/Client-Atlantic%20Recording%20Corporation-6366F1)

> **Executive Client:** Atlantic Recording Corporation  
> **Live Deployed Application:** [https://dhruvdekhane62-um-project1-app-uugher.streamlit.app/](https://dhruvdekhane62-um-project1-app-uugher.streamlit.app/)  
> **GitHub Repository:** [https://github.com/DhruvDekhane62/UM_project1](https://github.com/DhruvDekhane62/UM_project1)  
> **Dataset Timeframe:** May 18, 2024 – November 27, 2025 (555 Snapshot Days, 27,800 Track-Day Observations)

---

## 📌 Executive Summary & Key Links

This repository contains the complete quantitative market intelligence suite engineered for **Atlantic Recording Corporation**. Shifting focus away from US-centric popularity forecasting, this analysis evaluates the structural, cultural, and format dynamics of the Spotify United Kingdom Top 50 daily playlist.

### 📄 Primary Project Deliverables
- 🚀 **Live Interactive Web Application:** [https://dhruvdekhane62-um-project1-app-uugher.streamlit.app/](https://dhruvdekhane62-um-project1-app-uugher.streamlit.app/)
- 📄 **Full Academic Research Paper:** [`paper/paper.md`](paper/paper.md)
- 📋 **Strategic Executive Briefing:** [`paper/executive_summary.md`](paper/executive_summary.md)
- 📊 **Exported Empirical Data Tables:** [`outputs/tables/`](outputs/tables/)
- 📑 **Data Dictionary & Validation Reports:** [`docs/data_quality.md`](docs/data_quality.md) | [`docs/data_dictionary.md`](docs/data_dictionary.md)

---

## 📊 Core Empirical Findings & Market Indicators

| Market Structure Indicator | Empirical Metric | Operational Insight & Business Impact |
| :--- | :--- | :--- |
| **Market Concentration (HHI)** | **`0.0112`** | Unconcentrated, highly competitive market structure; no oligopoly locking the chart. |
| **Content Variety Index** | **`0.8510`** | High artist diversity score (Normalized Shannon Entropy across 370 unique artists). |
| **Top 5 Artist Share** | **`14.89%`** | Combined credit share of top 5 acts (Taylor Swift, Sabrina Carpenter, Billie Eilish, Olivia Rodrigo, Chappell Roan). |
| **Album vs. Single Ratio** | **`59.96% Album` vs `39.76% Single`** | Deep album campaigns drive nearly 60% of chart presence via multi-track surge retention. |
| **Top 10 Explicit Share** | **`40.40%`** | Explicit content spikes significantly in elite Top 10 ranks compared to Rest 11–50 (`29.97%`). |
| **Explicit Popularity Penalty** | **`Zero` (86.71 vs 86.83)** | UK listeners display zero aversion to explicit lyrics in top chart tiers. |
| **Collaboration Baseline** | **`19.26%`** | Stable multi-artist collaboration baseline maintained across all chart tiers. |
| **Optimal Track Duration** | **`< 2:30 min` (87.77 Mean Pop)** | Short-form formatting achieves peak popularity; tracks > 4:30 drop off to 84.08 mean pop. |

---

## 🎯 Strategic Recommendations for Atlantic Recording Corporation

1. **Prioritize Album Rollouts over Standalone Singles:** With **59.96%** of charting tracks stemming from parent albums, full album releases generate sustained catalog streaming revenue over months.
2. **Authorize Uncensored Explicit Lead Singles:** Top 10 tracks feature **40.40% explicit content** with zero popularity penalty. Uncensored releases increase youth demographic resonance in the UK market.
3. **Pair International Signees with Established UK Acts:** Leverage the **19.26% collaboration baseline** to pair emerging global signees with domestic UK acts for immediate playlist entry.
4. **Target 2:00 – 3:15 Track Duration Window:** Short tracks under 2:30 record the highest mean popularity score (`87.77`), optimizing repeat plays and streaming algorithm recommendations.

---

## 🛠️ Project Architecture & Directory Structure

```
uk-top50-project/
├── app.py                     # Streamlit application main entry point
├── requirements.txt           # Python dependency definitions
├── .streamlit/
│   └── config.toml            # Streamlit theme & headless server configuration
├── src/                       # Core Python analytical source modules
│   ├── load.py                # Data loading, cleaning, & parquet caching
│   ├── metrics.py             # Pure analytical KPI engines (HHI, Entropy, Leaders)
│   ├── charts.py              # Plotly figure generators & PyVis network builders
│   ├── validate.py            # Automated data quality & constraint validator
│   └── artist_exceptions.py   # Regex exception rules for multi-word band names
├── paper/                     # Publication deliverables
│   ├── paper.md               # Full quantitative research paper
│   └── executive_summary.md   # Executive C-suite briefing
├── outputs/                   # Exported research artifacts
│   ├── tables/                # CSV exported metric summary tables
│   └── figures/               # Static rendered chart figures
├── docs/                      # Technical & data documentation
│   ├── data_quality.md        # Automated data quality report
│   ├── data_dictionary.md     # Column definitions and data types
│   └── artist_delimiter_review.md # Multi-artist delimiter audit
├── tests/                     # Automated unit test suite
│   ├── test_load.py           # Unit tests for data loading & artist splitting
│   └── test_metrics.py        # Unit tests for metric calculations
└── data/
    ├── raw/                   # Raw unedited dataset (uk_top50.csv)
    └── processed/             # Cleaned high-performance parquet dataset
```

---

## 💻 Streamlit Web Application Features

The interactive web dashboard ([https://dhruvdekhane62-um-project1-app-uugher.streamlit.app/](https://dhruvdekhane62-um-project1-app-uugher.streamlit.app/)) includes five core analytical views:

1. **🎤 Artist Dominance:** Top 15 leaderboard, artist credit shares, daily unique artist trendlines, HHI concentration index, and Shannon entropy.
2. **🤝 Collaborations:** Rank group collaboration ratios (Top 10 vs Rest 11–50) and an interactive **PyVis network graph** mapping co-credits.
3. **🔞 Explicit Content:** Rank group explicitness distribution and Spotify popularity comparisons (Explicit vs Clean).
4. **💿 Release Formats:** Single vs Album donut charts and distribution histograms of total tracks on parent releases.
5. **⏱️ Track Duration:** Duration bucket histograms and average popularity analysis across length categories.
6. **🔍 Global Filters:** Dynamic sidebar controls for Date Range, Specific Artist(s), Track Type (Solo vs Collab), and Release Format.

---

## ⚙️ Local Installation & Execution

### Prerequisites
- Python 3.11+
- Git

### Quickstart Guide

```bash
# 1. Clone the repository
git clone https://github.com/DhruvDekhane62/UM_project1.git
cd UM_project1

# 2. Create and activate a virtual environment
python -m venv .venv
# On Windows: .venv\Scripts\activate
# On macOS/Linux: source .venv/bin/activate

# 3. Install required packages
pip install -r requirements.txt

# 4. Launch the local Streamlit dashboard
streamlit run app.py
```

---

## 🧪 Automated Testing & Data Validation

Run the test suite and validation scripts locally:

```bash
# Run all unit tests
pytest -v

# Run data validation pipeline and generate quality report
python -m src.validate
```

---

## 📜 License & Acknowledgments

Developed for **Atlantic Recording Corporation** as part of the **Unified Mentor Project One** curriculum.  
All data derived from daily Spotify UK Top 50 playlist snapshots (May 2024 – November 2025).
