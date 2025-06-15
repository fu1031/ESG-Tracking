'''import pandas as pd
import time
import pickle
import os
from newspaper import Article
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm
import datetime
# === CONFIG ===
INPUT_CSV = "linkedin_esg_weekly_summary.csv"
OUTPUT_CSV = "linkedin_esg_weekly_summary_final.csv"
COOKIE_FILE = "linkedin_cookies.pkl"
SLEEP_BETWEEN_LINKS = 2

# === Setup Selenium Headless Browser ===
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=options)

# === Visit LinkedIn Homepage and Load Cookies ===
driver.get("https://www.linkedin.com")
time.sleep(5)

if os.path.exists(COOKIE_FILE):
    with open(COOKIE_FILE, "rb") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            if 'sameSite' in cookie and cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
            try:
                driver.add_cookie(cookie)
            except Exception:
                continue
    driver.refresh()
    time.sleep(3)
else:
    print("No cookie file found. Please manually login and save cookies using a separate script if needed.")
    driver.quit()
    exit()

# === Load Data ===
df = pd.read_csv(INPUT_CSV)
all_intermediate_urls = []
all_final_urls = []
all_texts = []

# === Process Each Row ===
for links in tqdm(df['Links'], desc="Processing links"):
    link_list = str(links).split(", ")
    resolved_intermediates = []
    resolved_final_urls = []
    extracted_texts = []

    for short_url in link_list:
        try:
            # Step 1: Go to lnkd.in and get intermediate redirection
            driver.get(short_url)
            time.sleep(SLEEP_BETWEEN_LINKS)

            a_tag = driver.find_element(By.CSS_SELECTOR, "a[href^='https://']")
            intermediate_url = a_tag.get_attribute("href")

            # Step 2: Final URL (could involve more redirection if needed)
            driver.get(intermediate_url)
            time.sleep(2)
            final_url = driver.current_url

            # Step 3: Extract article content
            article = Article(final_url)
            article.download()
            article.parse()
            preview = article.text.strip()[:500]

        except Exception as e:
            intermediate_url = short_url
            final_url = short_url
            preview = f"Error: {e}"

        resolved_intermediates.append(intermediate_url)
        resolved_final_urls.append(final_url)
        extracted_texts.append(preview)

    all_intermediate_urls.append(" ||| ".join(resolved_intermediates))
    all_final_urls.append(" ||| ".join(resolved_final_urls))
    all_texts.append(" ||| ".join(extracted_texts))

# === Save to CSV ===
df["Intermediate URL"] = all_intermediate_urls
df["Final URL"] = all_final_urls
df["Preview Text"] = all_texts
df.to_csv(OUTPUT_CSV, index=False)
print(f"Done! Results saved to {OUTPUT_CSV}")

# Cleanup
driver.quit()'''
import pandas as pd
import time
import pickle
import os
from newspaper import Article
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm
import datetime

# === CONFIG ===
INPUT_CSV = "linkedin_esg_weekly_summary.csv"
OUTPUT_CSV = "linkedin_esg_weekly_summary_cleaned.csv"
COOKIE_FILE = "linkedin_cookies.pkl"
SLEEP_BETWEEN_LINKS = 2

# === Setup Selenium Headless Browser ===
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=options)

# === Visit LinkedIn Homepage and Load Cookies ===
driver.get("https://www.linkedin.com")
time.sleep(5)

if os.path.exists(COOKIE_FILE):
    with open(COOKIE_FILE, "rb") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            if cookie.get('sameSite') == 'None':
                cookie['sameSite'] = 'Strict'
            try:
                driver.add_cookie(cookie)
            except Exception:
                continue
    driver.refresh()
    time.sleep(3)
else:
    print("Cookie file not found. Please login manually or run a cookie-saving script first.")
    driver.quit()
    exit()

# === Load Input CSV ===
df = pd.read_csv(INPUT_CSV)

# Prepare lists to collect output
titles, previews, final_urls, dates = [], [], [], []

# === Process Each Row ===
for links in tqdm(df['Links'], desc="Processing links"):
    link_list = str(links).split(", ")
    # default placeholders
    article_title = None
    article_preview = None
    article_url = None

    today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    for short_url in link_list:
        try:
            # Step 1: Go to intermediate link
            driver.get(short_url)
            time.sleep(SLEEP_BETWEEN_LINKS)

            a_tag = driver.find_element(By.CSS_SELECTOR, "a[href^='http']")
            intermediate = a_tag.get_attribute("href")

            # Step 2: Follow to final URL
            driver.get(intermediate)
            time.sleep(2)
            resolved_url = driver.current_url

            # Step 3: Extract article using newspaper
            art = Article(resolved_url)
            art.download()
            art.parse()
            title = art.title.strip()
            preview = art.text.strip()[:500]

            # only take the first valid result
            if title and preview:
                article_title = title
                article_preview = preview
                article_url = resolved_url
                break

        except Exception:
            continue

    # if any critical piece is missing, skip row
    if not all([article_title, article_preview, article_url]):
        continue

    titles.append(article_title)
    previews.append(article_preview)
    final_urls.append(article_url)
    dates.append(today_str)

driver.quit()

# === Build Output DataFrame ===
clean_df = pd.DataFrame({
    "Title": titles,
    "Preview Text": previews,
    "URL": final_urls,
    "Date": dates
})

clean_df.to_csv(OUTPUT_CSV, index=False)
print(f"Cleaned CSV with Titles saved to '{OUTPUT_CSV}'.")