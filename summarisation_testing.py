import pandas as pd
import cohere
from tqdm import tqdm

API_KEY = "2gjGnyG7Oourqr7BlBo6YV7S4BRbf2JZp75io4Pt"  
MODEL = "command-light"   # Free tier model
INPUT_CSV = "linkedin_esg_weekly_summary_tagged.csv"
OUTPUT_CSV = "linkedin_esg_weekly_summary_tagged_with_summary.csv"

co = cohere.Client(API_KEY)

df = pd.read_csv(INPUT_CSV)
texts = df["Preview Text"].fillna("").tolist()
summaries = []

# Generate summaries
for text in tqdm(texts, desc="Summarizing articles"):
    if not text.strip():
        summaries.append("No content available.")
        continue

    try:
        prompt = f"Summarize the following ESG article in 1–2 sentences focusing on key insights:\n\n{text[:1500]}"
        response = co.generate(
            model=MODEL,
            prompt=prompt,
            max_tokens=100,
            temperature=0.4
        )
        summary = response.generations[0].text.strip()
    except Exception as e:
        summary = f"Error: {e}"

    summaries.append(summary)

df["Summary"] = summaries
df.to_csv(OUTPUT_CSV, index=False)
print(f"Done! Summaries saved to '{OUTPUT_CSV}'")