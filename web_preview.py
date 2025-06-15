import pandas as pd
from newspaper import Article
from tqdm import tqdm
import time

df = pd.read_csv("esg_titles_cleaned.csv")

# Drop rows with missing or duplicated URLs
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
        if not content or "404" in content.lower() or "not found" in content.lower() or "access denied" in content.lower():
            extracted_texts.append("")  
        else:
            extracted_texts.append(content)
    except Exception as e:
        extracted_texts.append("")  # Mark failed entries as empty
    time.sleep(1) 

df['Preview Text'] = extracted_texts
df = df[df['Preview Text'].str.strip().astype(bool)]  # Keep only rows with non-empty preview text

df.to_csv("esg_titles_contents.csv", index=False)
print("Cleaned and filtered ESG titles saved to 'esg_titles_contents.csv'")