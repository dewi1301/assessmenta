from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sqlite3
from datetime import datetime
import time

options = webdriver.ChromeOptions()
options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
# Remove "--headless" for debugging
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Install the correct ChromeDriver automatically
service = Service(ChromeDriverManager().install())

# Launch Chrome with Selenium
driver = webdriver.Chrome(service=service, options=options)

driver.set_page_load_timeout(120)

# Visit the target URL
URL = "https://www.theverge.com/tech"
driver.get(URL)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# Wait for content to load
time.sleep(10)

# Check page title
print("Page Title:", driver.title)

# Scrape articles
articles = driver.find_elements(By.CSS_SELECTOR, "_1xwtict9 _1pm20r55 _1pm20r52")

data = []
for article in articles:
    title = article.text.strip()
    link = article.get_attribute("href")
    date_str = datetime.now().strftime("%Y-%m-%d")  # The Verge doesn't display exact dates
    data.append((title, link, date_str))

# Quit the driver after scraping
driver.quit()

# Save to SQLite
def save_to_db(data):
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS headlines (title TEXT, link TEXT, date TEXT)")
    
    for title, link, date in data:
        c.execute("INSERT INTO headlines (title, link, date) VALUES (?, ?, ?)", (title, link, date))
    
    conn.commit()
    conn.close()

save_to_db(data)
print(f"Scraping completed! {len(data)} articles saved.")