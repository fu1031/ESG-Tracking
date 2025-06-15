from selenium import webdriver
import time
import pickle
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--window-size=1920,1080")
# Do NOT use headless here — you need the browser to pop up

driver = webdriver.Chrome(options=options)
driver.get("https://www.linkedin.com/login")

print("⚠️ Please log in manually within the next 90 seconds...")
time.sleep(90)  # Give yourself more time if needed

with open("linkedin_cookies.pkl", "wb") as file:
    pickle.dump(driver.get_cookies(), file)

print("✅ Cookies saved successfully.")
driver.quit()