import pandas as pd
import cohere
from tqdm import tqdm
from newspaper import Article

# === CONFIG ===
API_KEY = "2gjGnyG7Oourqr7BlBo6YV7S4BRbf2JZp75io4Pt"
MODEL = "command-light"
INPUT_CSV = "esg_titles_contents.csv"
OUTPUT_CSV = "esg_titles_contents_with_summary_cleaned.csv"

# === Init ===
co = cohere.Client(API_KEY)
df = pd.read_csv(INPUT_CSV)

# === Clean up rows with bad or empty content ===
df = df[~df["Preview Text"].str.lower().str.contains("404|error|not found", na=False)]
df = df[df["Preview Text"].str.strip().astype(bool)]  # Remove empty or whitespace rows

# === Summarize Preview Text ===
summaries = []
for text in tqdm(df["Preview Text"], desc="Summarizing"):
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

# === Extract Article Titles from URLs ===
titles = []
for url in tqdm(df["URL"], desc="Extracting titles"):
    try:
        article = Article(url)
        article.download()
        article.parse()
        titles.append(article.title.strip())
    except Exception:
        titles.append("Title not available")

# === Final Output ===
df["Article Title"] = titles
df["Summary"] = summaries

final_df = df[["Article Title", "Preview Text", "Summary", "URL"]]
final_df.to_csv(OUTPUT_CSV, index=False)
print(f"Cleaned output saved to '{OUTPUT_CSV}'")