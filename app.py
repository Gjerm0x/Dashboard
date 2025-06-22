import streamlit as st
import pandas as pd
from sqlalchemy import create_engine,inspect
import urllib
import altair as alt
from pathlib import Path

BASE_DIR=Path.cwd()
DB_PATH = BASE_DIR/ "Streamlit_Dash_Salaries"  / "analytics.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
print("Working dir:", Path.cwd())
print("Looking for DB at:", DB_PATH)
inspector = inspect(engine)
print("Found tables:", inspector.get_table_names())
df = pd.read_sql("SELECT * FROM careers_raw", engine)

# 2. Load tables
@st.cache_data(ttl=300)
def load_table(name):
    query = f"Select * FROM {name}"
    return pd.read_sql_query(query, engine)

raw  = load_table("careers_raw")
reg  = load_table("meaning_vs_salary")
cat  = load_table("category_summary")

# 3. UI
st.title("Career Analysis Dashboard")

st.header("Raw Data by Rank")
st.dataframe(raw)

st.header("Meaning vs Salary Regression")
chart = (
    alt.Chart(reg)
    .transform_regression('% High Meaning', 'Mid-Career Pay', method="linear", as_=['% High Meaning', 'Predicted Salary'])
    .mark_line(color='green')
    .encode(x='% High Meaning:Q', y='Predicted Salary:Q')
    +
    alt.Chart(reg)
    .mark_circle(size=60)
    .encode(
        x='% High Meaning:Q',
        y='Mid-Career Pay:Q',
        tooltip=['Major:N', '% High Meaning:Q', 'Mid-Career Pay:Q']
    )
)
st.altair_chart(chart.interactive(), use_container_width=True)


st.header("Category Summary")
st.bar_chart(cat.set_index("Category")["Mid-Career Pay"])