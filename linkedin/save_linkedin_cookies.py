# save_linkedin_cookies.py
import pickle, time, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

COOKIE_FILE = "linkedin_cookies.pkl"

def main():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.linkedin.com/login")
    print("👉 Please log in manually.")
    while "feed" not in driver.current_url:
        time.sleep(2)

    with open(COOKIE_FILE, "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print(f"✅ Cookies saved to {COOKIE_FILE}")

    driver.quit()

if __name__ == "__main__":
    main()