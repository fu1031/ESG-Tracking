import pandas as pd
import cohere
from tqdm import tqdm
from newspaper import Article
import re

# === CONFIG ===
API_KEY = "2gjGnyG7Oourqr7BlBo6YV7S4BRbf2JZp75io4Pt"
MODEL = "command-light"
INPUT_CSV = "esg_titles_contents_tagged.csv"
OUTPUT_CSV = "esg_titles_contents_with_summary_cleaned.csv"

# === INIT ===
co = cohere.Client(API_KEY)
df = pd.read_csv(INPUT_CSV)

# === Cleanup invalid rows ===
df = df[~df["Preview Text"]
        .str.lower()
        .str.contains("404|error|not found", na=False)]
df = df[df["Preview Text"].str.strip().astype(bool)]

# === Filter out irrelevant marketing-style intros ===
patterns = [
    r"discover how", 
    r"welcome to [^ ]+’s debried", 
    r"gain insights into", 
    r"learn more at", 
    r"get started with"
]
regex = re.compile('|'.join(patterns), re.IGNORECASE)
df = df[~df["Preview Text"].str.match(regex)]

# === Deduplicate ===
df = df.drop_duplicates(subset=["URL", "Preview Text"])

# === Summaries ===
summaries = []
for text in tqdm(df["Preview Text"], desc="Summarizing"):
    try:
        prompt = (
            "Summarize the following ESG article in 1–2 sentences focusing on key insights:\n\n"
            f"{text[:1500]}"
        )
        resp = co.generate(model=MODEL, prompt=prompt, max_tokens=100, temperature=0.4)
        summaries.append(resp.generations[0].text.strip())
    except Exception as e:
        summaries.append(f"Error: {e}")
df["Summary"] = summaries

# === Titles ===
titles = []
for url in tqdm(df["URL"], desc="Extracting titles"):
    try:
        art = Article(url)
        art.download(); art.parse()
        titles.append(art.title.strip())
    except Exception:
        titles.append("Title not available")
df["Article Title"] = titles

# === Final Columns ===
final_df = df[[
    "Article Title",
    "Preview Text",
    "Predicted Tags",
    "Summary",
    "URL"
]]
final_df.to_csv(OUTPUT_CSV, index=False)
print(f"Cleaned output saved to '{OUTPUT_CSV}'")