import pandas as pd
from sqlalchemy import create_engine,inspect
import urllib
import sqlite3

# 1. Read & clean
file = pd.read_csv("final-post-college-salaries.csv")

# strip symbols and convert to numeric
file['Early Career Pay']= pd.to_numeric(file['Early Career Pay'].replace(r'[\$,]', '', regex=True),errors='coerce')
file['Mid-Career Pay']=pd.to_numeric(file['Mid-Career Pay'].replace(r'[\$,]', '', regex=True),errors='coerce')
file['% High Meaning']=pd.to_numeric(file['% High Meaning'].replace(r'[%]', '', regex=True),errors='coerce')

# categorize majors
def categorize_major(major):
    if any(k in major for k in ('Engineering','Computer','Math','Science')):
        return 'STEM'
    if any(k in major for k in ('Economics','Finance','Business','Accounting')):
        return 'Business'
    if any(k in major for k in ('Psychology','Sociology','Social')):
        return 'Social Sciences'
    if any(k in major for k in ('Art','Design','Theater','Music','Photography')):
        return 'Arts'
    if any(k in major for k in ('Education','Teaching')):
        return 'Education'
    return 'Other'

file['Category'] = file['Major'].apply(categorize_major)

# prepare regression DataFrame
clean_data = file[['Major','% High Meaning', 'Mid-Career Pay']].dropna(subset=['% High Meaning','Mid-Career Pay'])

# prepare category summary
category_summary = (
    file
    .groupby('Category')[['Mid-Career Pay','% High Meaning']]
    .mean()
    .reset_index()
)

odbc_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=SWERVOPC;DATABASE=AnalyticsDB;"
    "Trusted_Connection=yes;"
)

engine = create_engine("sqlite:///Analytics.db", echo=False)

file.to_sql(
    name="careers_raw",
    con=engine,
    if_exists="replace",
    index=False
)
clean_data.to_sql(
    name="meaning_vs_salary",
    con=engine,
    if_exists="replace",
    index=False
)
category_summary.reset_index().to_sql(
    name="category_summary",
    con=engine,
    if_exists="replace",
    index=False
)

conn = sqlite3.connect("analytics.db")
cur  = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
existing = {row[0] for row in cur.fetchall()}

expected = {"careers_raw", "meaning_vs_salary", "category_summary"}

if expected.issubset(existing):
    print("✅ ETL complete: all tables created successfully.")
else:
    missing = expected - existing
    raise RuntimeError(f"❌ ETL failed: missing tables {missing}")

conn.close()