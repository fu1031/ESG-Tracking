import pandas as pd
from newspaper import Article
from tqdm import tqdm
import time

# Load input
df = pd.read_excel("esg_titles_cleaned.xlsx")

# Drop missing or duplicate URLs
df = df.dropna(subset=['URL'])
df = df.drop_duplicates(subset='URL')

# Initialize extracted text list
extracted_texts = []

# Extract article content
for url in tqdm(df['URL'], desc="Extracting articles"):
    try:
        article = Article(url)
        article.download()
        article.parse()
        content = article.text.strip()

        # Filter out irrelevant or broken content
        if not content or any(term in content.lower() for term in ["404", "not found", "access denied"]):
            extracted_texts.append("")  
        else:
            extracted_texts.append(content)
    except Exception:
        extracted_texts.append("")  # Mark failed entries as empty
    time.sleep(1)

# Add column and filter out empty text rows
df['Preview Text'] = extracted_texts
df = df[df['Preview Text'].str.strip().astype(bool)]

# Save as Excel
output_file = "esg_titles_contents.xlsx"
df.to_excel(output_file, index=False)
print(f"✅ Cleaned and filtered ESG titles saved to '{output_file}'")
