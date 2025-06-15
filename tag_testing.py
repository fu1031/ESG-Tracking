import pandas as pd
import cohere
from tqdm import tqdm

API_KEY = "2gjGnyG7Oourqr7BlBo6YV7S4BRbf2JZp75io4Pt"  
MODEL = "command-light"  # Trial accounts support this model
INPUT_CSV = "/Users/raofu/Desktop/ESG_Tracking/linkedin/linkedin_esg_weekly_summary_final.csv"
OUTPUT_CSV = "linkedin_esg_weekly_summary_tagged.csv"

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

co = cohere.Client(API_KEY)

df = pd.read_csv(INPUT_CSV)
preview_texts = df["Preview Text"].fillna("").tolist()
predicted_tags = []

# Loop through each preview
# Revised prompt logic for hierarchical tagging
for text in tqdm(preview_texts, desc="Tagging articles"):
    if not text.strip():
        predicted_tags.append("Empty text")
        continue

    try:
        prompt = f"""You are a sustainability analyst. Based on the ESG article content below, identify:
1. The most relevant **main ESG category**.
2. One or more matching **sub-topic tags** from that category.

Please follow this structure strictly:
Category: <Main Category>
Tags: <comma-separated sub-topic tags>

Available categories and sub-tags:
- Carbon Markets / Pricing: [Carbon credits, Carbon tax, Carbon trading schemes, Voluntary carbon markets, Carbon offset projects, Carbon neutrality targets]
- Climate Change & Mitigation: [Climate adaptation, Climate risk disclosures, Climate policy updates, Sea level rise, Ocean acidification, Emissions reduction pathways, Net-zero targets]
- ESG Regulations & Reporting: [ESG regulations (global, EU, Asia, US), ESG disclosures (CSRD, SFDR, TCFD, SEC), Mandatory vs voluntary reporting, Sustainability reporting frameworks, Greenwashing risks & cases, ESG data quality and assurance]
- Corporate Sustainability: [Corporate net-zero pledges, Corporate ESG initiatives, Supply chain sustainability, Green finance, ESG investing trends]
- Biodiversity & Nature: [Nature-based solutions, Biodiversity credits, Ecosystem services markets, Conservation finance]
- Ocean & Marine Topics: [Ocean acidification, Marine biodiversity, Ocean health policy]
- Environmental Laws & Compliance: [EHS compliance, Pollution regulations, Waste management, Circular economy, Water regulation]
- Social & Governance: [Human rights, Supply chain due diligence, ESG-linked executive pay, Board ESG oversight, Labor practices, Diversity]
- General Market Trends: [Green technology, ESG data providers, ESG litigation, Climate-related financial risks]

ESG Article:
\"\"\"{text[:1500]}\"\"\"

Now respond:
Category:"""

        response = co.generate(
            model=MODEL,
            prompt=prompt,
            max_tokens=120,
            temperature=0.5
        )
        prediction = response.generations[0].text.strip()
    except Exception as e:
        prediction = f"Error: {str(e)}"

    predicted_tags.append(prediction)
# Add results
df["Predicted Tags"] = predicted_tags
df.to_csv(OUTPUT_CSV, index=False)
print(f"Done! Tagged results saved to '{OUTPUT_CSV}'")