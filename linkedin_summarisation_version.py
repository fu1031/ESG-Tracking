import pandas as pd
import cohere
from tqdm import tqdm
from newspaper import Article

API_KEY = "2gjGnyG7Oourqr7BlBo6YV7S4BRbf2JZp75io4Pt"
MODEL = "command-light"
INPUT_CSV = "linkedin_esg_weekly_summary_tagged.csv"
OUTPUT_CSV = "linkedin_esg_weekly_summary_tagged_with_summary.csv"

co = cohere.Client(API_KEY)

df = pd.read_csv(INPUT_CSV)

# Drop rows with missing, error, or irrelevant preview text
def is_valid_text(txt):
    if not isinstance(txt, str):
        return False
    txt = txt.lower()
    return (
        "404" not in txt
        and "not found" not in txt
        and "error" not in txt
        and "this link will take you to a page" not in txt
        and len(txt.strip()) > 20
    )

df = df[df["Preview Text"].apply(is_valid_text)].copy()

# Extract the last Final URL from 'Final URL' column
df["URL"] = df["Final URL"].apply(lambda x: str(x).split("|||")[-1].strip())

# Fetch article title
titles = []
for url in tqdm(df["URL"], desc="Fetching titles"):
    try:
        article = Article(url)
        article.download()
        article.parse()
        titles.append(article.title.strip())
    except Exception as e:
        titles.append("Error extracting title")

df["Article Title"] = titles

# Summarize each article
texts = df["Preview Text"].tolist()
summaries = []

for text in tqdm(texts, desc="Summarizing articles"):
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

# Save selected columns in desired order
output_df = df[["Article Title", "Preview Text", "Predicted Tags", "Summary", "URL"]]
output_df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Done! Cleaned and summarized file saved to '{OUTPUT_CSV}'")