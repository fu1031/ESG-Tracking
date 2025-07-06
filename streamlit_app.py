import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="ESG‑Tracking Dashboard", layout="wide")
st.title("📊 ESG Tracking Dashboard")

# === ESG Tags list ===
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

# === Region keywords ===
REGIONS = ["Singapore", "Asia", "APAC", "Europe", "EU", "United States", "US", "Global"]

# === Climate keywords ===
CLIMATE_TOPICS = [
    "Ocean acidification", "Global warming", "Sea level rise", "Melting ice caps", "Climate change",
    "Extreme weather", "Temperature rise", "Greenhouse gas emissions", "Climate resilience",
    "Methane leakage", "Climate tipping points", "El Niño", "La Niña"
]

# === Load final output files ===
try:
    df_web = pd.read_excel("esg_titles_contents_with_summary_cleaned.xlsx")
    df_linkedin = pd.read_excel("linkedin_esg_weekly_summary_tagged_with_summary.xlsx")
except FileNotFoundError as e:
    st.error(f"Could not load data: {e}")
    st.stop()

# === Sidebar filters ===
st.sidebar.header("Filters")
tag_filter = st.sidebar.multiselect("Select ESG Tags", TAGS)
region_filter = st.sidebar.multiselect("Select Region Keywords", REGIONS)
climate_filter = st.sidebar.multiselect("Select Climate Topics", CLIMATE_TOPICS)

# === Display web content ===
st.subheader("🌐 Web-scraped ESG Articles")
df_web_filtered = df_web.copy()

if region_filter:
    df_web_filtered = df_web_filtered[
        df_web_filtered["Preview Text"].str.contains("|".join(region_filter), case=False, na=False)
        | df_web_filtered["Summary"].str.contains("|".join(region_filter), case=False, na=False)
    ]

if climate_filter:
    df_web_filtered = df_web_filtered[
        df_web_filtered["Preview Text"].str.contains("|".join(climate_filter), case=False, na=False)
        | df_web_filtered["Summary"].str.contains("|".join(climate_filter), case=False, na=False)
    ]

expected_cols = ["Article Title", "Predicted Tags", "Summary", "URL", "Preview Text"]
df_web_filtered = df_web_filtered[[col for col in expected_cols if col in df_web_filtered.columns]]
st.dataframe(df_web_filtered, height=300)

# === LinkedIn summaries ===
st.subheader("🔗 LinkedIn ESGPedia Summaries")
df_linkedin_filtered = df_linkedin.copy()

if tag_filter:
    df_linkedin_filtered = df_linkedin_filtered[
        df_linkedin_filtered["Predicted Tags"].str.contains("|".join(tag_filter), case=False, na=False)
    ]

if region_filter:
    df_linkedin_filtered = df_linkedin_filtered[
        df_linkedin_filtered["Preview Text"].str.contains("|".join(region_filter), case=False, na=False)
        | df_linkedin_filtered["Summary"].str.contains("|".join(region_filter), case=False, na=False)
    ]

if climate_filter:
    df_linkedin_filtered = df_linkedin_filtered[
        df_linkedin_filtered["Preview Text"].str.contains("|".join(climate_filter), case=False, na=False)
        | df_linkedin_filtered["Summary"].str.contains("|".join(climate_filter), case=False, na=False)
    ]

df_linkedin_filtered = df_linkedin_filtered[[col for col in expected_cols if col in df_linkedin_filtered.columns]]
st.dataframe(df_linkedin_filtered, height=300)

# === Download options ===
st.markdown("---")
st.markdown("### 📥 Download Data")

web_buffer = io.BytesIO()
df_web_filtered.to_excel(web_buffer, index=False, engine='openpyxl')
web_buffer.seek(0)

linkedin_buffer = io.BytesIO()
df_linkedin_filtered.to_excel(linkedin_buffer, index=False, engine='openpyxl')
linkedin_buffer.seek(0)

st.download_button(
    label="Download Web Excel File",
    data=web_buffer,
    file_name="esg_web.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.download_button(
    label="Download LinkedIn Excel File",
    data=linkedin_buffer,
    file_name="esg_linkedin.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)