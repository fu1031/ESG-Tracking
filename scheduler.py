# scheduler.py
import schedule
import time
import subprocess

def run_all():
    print("🟢 Running ESG pipeline...")
    scripts = [
        "python web_title_url_extraction.py",
        "python web_preview.py",
        "python tag_testing.py",
        "python summarisation_testing.py",
        "python linkedin/linkedin_content.py"
    ]
    for cmd in scripts:
        print(f"🔁 {cmd}")
        subprocess.run(cmd, shell=True)
    print("✅ Pipeline complete.\n")

# Schedule twice weekly (e.g., Monday & Thursday at 2 AM)
schedule.every().monday.at("02:00").do(run_all)
schedule.every().thursday.at("02:00").do(run_all)

# Or monthly, choose one:
# schedule.every().month.at("02:00").do(run_all)

if __name__ == "__main__":
    run_all()
    while True:
        schedule.run_pending()
        time.sleep(60)