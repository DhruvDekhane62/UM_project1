# United Kingdom Top 50 Playlist Market Structure & Content Localization Analysis

**Client:** Atlantic Recording Corporation  
**Live Application URL:** [https://dhruvdekhane62-um-project1-app-uugher.streamlit.app/](https://dhruvdekhane62-um-project1-app-uugher.streamlit.app/)  

---

## 📌 Executive Deliverables
- 🚀 **Live Streamlit Web App:** [https://dhruvdekhane62-um-project1-app-uugher.streamlit.app/](https://dhruvdekhane62-um-project1-app-uugher.streamlit.app/)
- 📄 **Full Research Paper:** [`paper/paper.md`](paper/paper.md)
- 📋 **Executive Summary Briefing:** [`paper/executive_summary.md`](paper/executive_summary.md)
- 📊 **Exported Metrics Tables:** [`outputs/tables/`](outputs/tables/)

---

## 🎵 Project Overview
This project delivers a market structure analysis of the Spotify United Kingdom Top 50 daily streaming playlist for Atlantic Recording Corporation. Analyzing 27,800 track-day observations across 555 consecutive snapshot days (May 18, 2024 – Nov 27, 2025), this study evaluates market concentration, artist diversity, collaboration dynamics, explicitness, release format dominance, and track duration preferences.

### Key Analytical Findings
- **Market Concentration (HHI):** `0.0112` (Highly competitive, non-monopolistic roster distribution)
- **Content Variety Index (Shannon Entropy):** `0.8510` (High artist diversity score)
- **Album vs. Single Share:** **59.96%** of charting tracks originate from full albums vs **39.76%** standalone singles.
- **Top 10 Explicit Share:** **40.40%** explicit content in the elite Top 10 tier with zero popularity penalty.
- **Collaboration Baseline:** **19.26%** overall chart presence across ranks.

---

## 🛠️ Tech Stack & Setup
- **Language:** Python 3.11+
- **Data Engineering:** pandas, numpy, pyarrow
- **Visualizations:** Plotly, PyVis (Interactive Network Graphs)
- **Web Framework:** Streamlit
- **Testing:** pytest

### Running Locally
```bash
# Clone the repository
git clone https://github.com/DhruvDekhane62/UM_project1.git
cd UM_project1

# Install dependencies
pip install -r requirements.txt

# Launch local dashboard
streamlit run app.py
```
