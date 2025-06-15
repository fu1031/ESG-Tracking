# streamlit_app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="ESG‑Tracking Dashboard", layout="wide")
st.title("📊 ESG Tracking Dashboard")

# ESG Tags list
TAGS = [
    "Carbon credits", "Carbon tax", "Carbon trading schemes", "Voluntary carbon markets", "Carbon offset projects",
    "Carbon neutrality targets", "Climate adaptation", "Climate risk disclosures", "Climate policy updates",
    "Sea level rise", "Ocean acidification", "Emissions reduction pathways", "Net-zero targets",
    "ESG regulations (global, EU, Asia, US)", "ESG disclosures (CSRD, SFDR, TCFD, SEC)", "Mandatory vs voluntary reporting",
    "Sustainability reporting frameworks", "Greenwashing risks & cases", "ESG data quality and assurance",
    "Corporate net-zero pledges", "Corporate ESG initiatives", "Supply chain sustainability", "Green finance",
    "ESG investing trends", "Nature-based solutions", "Biodiversity credits", "Ecosystem services markets",
    "Conservation finance", "Marine biodiversity", "Ocean health policy", "EHS compliance",
    "Pollution regulations", "Waste management", "Circular economy", "Water regulation",
    "Human rights", "Supply chain due diligence", "ESG-linked executive pay", "Board ESG oversight",
    "Labor practices", "Diversity", "Green technology", "ESG data providers", "ESG litigation",
    "Climate-related financial risks"
]

# Load final output files
try:
    df_web = pd.read_csv("esg_titles_contents_with_summary_cleaned.csv")
    df_linkedin = pd.read_csv("linkedin_esg_weekly_summary_tagged_with_summary.csv")
except FileNotFoundError as e:
    st.error(f"Could not load data: {e}")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
tag_filter = st.sidebar.multiselect("Select ESG Tags", TAGS)

# Display web content
st.subheader("🌐 Web-scraped ESG Articles")
st.dataframe(df_web, height=300)

# LinkedIn summaries
st.subheader("🔗 LinkedIn ESGPedia Summaries")
df = df_linkedin.copy()

# Filter based on tags
if tag_filter:
    df = df[df['Predicted Tags'].str.contains("|".join(tag_filter), case=False, na=False)]

st.dataframe(df, height=300)

# Download options
st.markdown("---")
st.markdown("### 📥 Download Data")
st.download_button("Download Web CSV", df_web.to_csv(index=False), "esg_web.csv")
st.download_button("Download LinkedIn CSV", df_linkedin.to_csv(index=False), "esg_linkedin.csv")