# streamlit_app.py
import streamlit as st
import pandas as pd
from PIL import Image
import streamlit as st


img = Image.open("SLNG-Logo-Colour.png")
st.image(img, width=200)
st.set_page_config(page_title="ESG‑Tracking Dashboard", layout="wide")

st.title("ESG Tracking Dashboard")

# Load final output files
try:
    df_web = pd.read_csv("esg_titles_contents.csv")
    df_linkedin = pd.read_csv("linkedin_esg_weekly_summary_tagged_with_summary.csv")
except FileNotFoundError as e:
    st.error(f"Could not load data: {e}")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
min_date = st.sidebar.date_input("From date", value=None)
tag_filter = st.sidebar.multiselect("Tags", sorted(df_linkedin.columns[df_linkedin.columns.str.contains("Tag")]))

# Display web content
st.subheader("🌐 Web-scraped ESG Articles")
st.dataframe(df_web, height=300)

# LinkedIn summaries
st.subheader("🔗 LinkedIn ESGPedia Summaries")
df = df_linkedin.copy()
if min_date:
    df = df[df['Date'] >= pd.to_datetime(min_date)]
if tag_filter:
    df = df[df['Predicted Tags'].str.contains("|".join(tag_filter), na=False)]
st.dataframe(df, height=300)

# Download option
st.markdown("---")
st.markdown("### 📥 Download Data")
st.download_button("Download Web CSV", df_web.to_csv(index=False), "esg_web.csv")
st.download_button("Download LinkedIn CSV", df_linkedin.to_csv(index=False), "esg_linkedin.csv")