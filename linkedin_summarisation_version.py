import pandas as pd
import cohere
from tqdm import tqdm
from newspaper import Article

# === CONFIG ===
API_KEY = "2gjGnyG7Oourqr7BlBo6YV7S4BRbf2JZp75io4Pt"
MODEL = "command-light"  # Free-tier model
INPUT_CSV = "linkedin_esg_weekly_summary_tagged.csv"
OUTPUT_CSV = "linkedin_esg_weekly_summary_tagged_with_summary.csv"

# === INIT ===
co = cohere.Client(API_KEY)
df = pd.read_csv(INPUT_CSV)

# === FILTER OUT BAD ROWS ===
def is_valid_text(txt):
    if not isinstance(txt, str):
        return False
    t = txt.lower()
    return (
        "404" not in t
        and "not found" not in t
        and "error" not in t
        and "this link will take you to a page" not in t
        and len(t.strip()) > 20
    )

df = df[df["Preview Text"].apply(is_valid_text)].copy()

# === EXTRACT FINAL URL ===
df["URL"] = df["Final URL"].apply(lambda x: str(x).split("|||")[-1].strip())

# === FETCH ARTICLE TITLES ===
titles = []
for url in tqdm(df["URL"], desc="Fetching titles"):
    try:
        article = Article(url)
        article.download()
        article.parse()
        titles.append(article.title.strip())
    except Exception:
        titles.append("Error extracting title")
df["Article Title"] = titles

# === GENERATE SUMMARIES ===
summaries = []
for text in tqdm(df["Preview Text"], desc="Summarizing"):
    try:
        prompt = (
            "Summarize the following ESG article in 1–2 concise sentences focusing on the key insights:\n\n"
            f"{text[:1500]}"
        )
        response = co.generate(
            model=MODEL,
            prompt=prompt,
            max_tokens=100,
            temperature=0.4
        )
        summaries.append(response.generations[0].text.strip())
    except Exception as e:
        summaries.append(f"Error: {e}")
df["Summary"] = summaries

# === OUTPUT CSV ===
output_df = df[[
    "Article Title",
    "Preview Text",
    "Predicted Tags",
    "Summary",
    "URL"
]].drop_duplicates(subset=["URL", "Preview Text"])  # remove duplicates

output_df.to_csv(OUTPUT_CSV, index=False)
print(f"Done! Cleaned and summarized file saved to '{OUTPUT_CSV}'")