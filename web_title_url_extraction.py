# updated_web_title_extraction.py
# ---------------------------------------------------------------
# Web Title Extractor Script for ESG Web Tracking (Direct Scrape)
# ---------------------------------------------------------------
# Purpose:
#   - Scrapes titles and links from ESG-relevant pages.
#   - Filters based on ESG-related keywords.
#   - Removes boilerplate links and duplicate titles.
#   - Saves structured results to an Excel file.

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Target URLs for ESG content tracking
urls = [
    "https://oceanacidification.noaa.gov/",
    "https://goa-on.org/news/news.php",
    "https://sphera.com/resources/",
    "https://www.carbonbrief.org/",
    "https://www.ioc.unesco.org/en",
    "https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-9/",
    "https://www.nccs.gov.sg/media/",
    "https://ccrs.weather.gov.sg/publications-listing-page",
    "https://unfccc.int/about-us/reports-highlights/un-climate-change-quarterly-updates",
    "https://www.weather.gov.sg/home-all-news/?yearnews=2015",
    "https://www.pub.gov.sg/Resources/Publications",
    "https://www.ema.gov.sg/news-events/news?id=media-releases",
    "https://www.esgtoday.com/category/esg-news/"
]

# ESG-relevant keywords for title filtering
esg_keywords = [
    "esg", "sustainability", "climate", "carbon", "report", "green",
    "governance", "policy", "energy", "emissions", "scope 3", "net zero"
]

# Phrases to skip (irrelevant or boilerplate)
skip_phrases = [
    "learn more", "contact", "support", "login", "search", "menu", "resources",
    "subscribe", "newsroom", "careers", "events", "platform", "about", "home",
    "privacy", "cookies", "partners"
]

def is_meaningful_title(title):
    """Determine if the text is a useful ESG-related title."""
    t = title.lower().strip()
    if len(t.split()) < 3:
        return False
    if any(skip in t for skip in skip_phrases):
        return False
    if any(keyword in t for keyword in esg_keywords):
        return True
    return False

def extract_titles(base_url):
    """Scrape page and extract meaningful ESG-relevant titles + URLs."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(base_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        seen = set()

        for tag in soup.find_all(['a', 'h2', 'h3']):
            text = tag.get_text(strip=True)
            href = tag.get('href', '')

            if not text or href.startswith('#'):
                continue

            normalized_text = text.lower().strip()
            if normalized_text in seen:
                continue

            if is_meaningful_title(text):
                seen.add(normalized_text)
                if not href.startswith("http"):
                    href = base_url.rstrip("/") + "/" + href.lstrip("/")
                results.append((text, href))

        return results

    except Exception as e:
        print(f"❌ Failed to scrape {base_url}: {e}")
        return []

# === Scrape all URLs ===
all_titles = []
for site in urls:
    print(f"🔍 Scraping: {site}")
    titles = extract_titles(site)
    all_titles.extend(titles)

# === Deduplicate by lowercase title text ===
deduped_titles = list({(title.lower().strip(), url) for title, url in all_titles})
deduped_titles = [(title.title(), url) for title, url in deduped_titles]  # Title case cleanup
deduped_titles.sort()

# === Save to Excel ===
df = pd.DataFrame(deduped_titles, columns=["Title", "URL"])
df.to_excel("esg_titles_cleaned.xlsx", index=False)
print("✅ Cleaned, deduplicated ESG titles saved to 'esg_titles_cleaned.xlsx'")