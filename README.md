# Analytics Dashboard

A Streamlit-based dashboard for exploring and analyzing career salary data.

## Live Demo

👉 [View the live dashboard](https://dashboard-7tpwxqcudvfhvxmw8kkcsg.streamlit.app/)

## Description

This dashboard provides interactive tables and charts that let users:
- Inspect raw salary records from the `careers_raw` table.
- Slice and dice by major, career stage, or percentile.
- Visualize distributions, trends, and key summary statistics.

## Libraries & Tools

- **Streamlit** — for building the interactive web UI  
- **pandas** — for data manipulation and analysis  
- **SQLAlchemy** — to connect to and inspect the SQLite database  
- **SQLite** — as the lightweight data store (`analytics.db`)  
- **Pathlib** — for platform-independent file paths  
- **Python Standard Library** — for utilities and supporting logic  

_(Plus any charting library you included, e.g., Plotly, Altair, or Matplotlib.)_

## Methodology

1. **Data Storage**  
   All raw career and salary data lives in a local SQLite database (`analytics.db`).  

2. **ETL Pipeline**  
   - An `etl.py` script uses SQLAlchemy and pandas to **Extract** raw CSVs, **Transform** (clean, parse, type-convert), and **Load** into the database.  
   - This ensures a single source of truth and avoids repeated CSV parsing in the app.  

3. **Data Loading & Caching**  
   - In `app.py`, a `@st.cache_data(ttl=300)`-decorated function `load_table(name)` runs a `SELECT * FROM {name}` via pandas' `read_sql_query`.  
   - Caching boosts performance, preventing redundant database hits on every interaction.  

4. **Interactive UI**  
   - Users select tables, filters, and chart types via Streamlit widgets (e.g., `st.selectbox`, `st.slider`).  
   - DataFrames and charts render instantly in the sidebar and main panel.  

5. **Visualization**  
   - Leveraged Streamlit’s built-in chart functions (or Plotly/Altair) to plot bar charts, line graphs, and distributions.  
   - Key metrics (mean, median, percentiles) displayed alongside visuals for quick insights.  

6. **Deployment**  
   - The app is deployed on Streamlit Cloud:  
     `streamlit run app.py` → pushed to GitHub → linked to your Streamlit Cloud account.  
   - CI/CD automatically rebuilds on each commit to the connected repo.  

## Getting Started

1. **Clone the repo**  
   ```bash
   git clone https://github.com/yourusername/your-dashboard-repo.git
   cd your-dashboard-repo
