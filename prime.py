import os
import time
import random
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

SEEN_FILE = "seen_links_prime.txt"
LOG_FILE = "log.txt"
OUTPUT_DIR = "output_prime"

CATEGORIES = {
    "Action": "https://www.primevideo.com/region/{region}/storefront/action",
    "Comedy": "https://www.primevideo.com/region/{region}/storefront/comedy",
    "Drama": "https://www.primevideo.com/region/{region}/storefront/drama",
    "Sci-Fi": "https://www.primevideo.com/region/{region}/storefront/scifi",
    "Documentary": "https://www.primevideo.com/region/{region}/storefront/documentary"
}

def setup_browser():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scroll_to_bottom(driver, max_wait=60):
    print("📜 Scrolling to load more...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    start_time = time.time()
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height or (time.time() - start_time > max_wait):
            break
        last_height = new_height
    print("✅ Reached bottom.")

def extract_links(driver):
    anchors = driver.find_elements(By.TAG_NAME, "a")
    results = []
    for a in anchors:
        href = a.get_attribute("href")
        if href and "/detail/" in href:
            title = a.get_attribute("title") or a.get_attribute("alt") or a.text.strip()
            results.append((title or "Unknown Title", href))
    return list(set(results))

def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_seen(new_links):
    with open(SEEN_FILE, "a") as f:
        for title, link in new_links:
            f.write(link + "\n")

def save_links(new_links, mode_label):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_DIR}/prime_{mode_label}_{timestamp}.txt"
    with open(filename, "w") as f:
        for title, link in new_links:
            f.write(f"{title} — {link}\n")
    print(f"💾 Saved {len(new_links)} links to {filename}")

def write_log(message):
    with open(LOG_FILE, "a") as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {message}\n")

def process_extraction(driver, label, url):
    driver.get(url)
    time.sleep(3)
    scroll_to_bottom(driver)
    extracted = extract_links(driver)
    seen = load_seen()
    unique = [(title, link) for title, link in extracted if link not in seen]
    duplicates = len(extracted) - len(unique)

    if unique:
        save_links(unique, label)
        save_seen(unique)
        write_log(f"Added {len(unique)} new links from: {label}")
        print(f"📊 Found {len(unique)} new links. 🔁 Skipped {duplicates} duplicates.")
    else:
        print("⚠️ No new unique links found.")
        write_log(f"No new links found for: {label}")

def main():
    print("🛠️ Amazon Prime Scraper — Created by Mike | DRMLab.io Project")
    region = input("🌍 Enter your Prime Video region (e.g. eu, us, uk): ").strip().lower()
    driver = setup_browser()

    print("🌐 Opening Prime Video storefront...")
    driver.get(f"https://www.primevideo.com/region/{region}/storefront/")
    time.sleep(5)
    input("🔐 Log in manually, then press ENTER to continue...")

    while True:
        print("\n📋 === MAIN MENU ===")
        print("1️⃣  Extract from storefront")
        print("2️⃣  Search by keyword")
        print("3️⃣  Browse by genre")
        print("4️⃣  Exit")
        choice = input("➡️ Enter your choice: ").strip()

        if choice == "1":
            process_extraction(driver, "storefront", f"https://www.primevideo.com/region/{region}/storefront/")
        elif choice == "2":
            keyword = input("🔍 Enter search keyword (or leave blank for random): ").strip()
            if not keyword:
                keyword = random.choice(["war", "love", "moon", "dark", "fire", "life", "death", "dream"])
                print(f"🎲 Using random keyword: {keyword}")
            url = f"https://www.primevideo.com/region/{region}/search/ref=atv_nb_sr?phrase={keyword}"
            process_extraction(driver, f"search_{keyword}", url)
        elif choice == "3":
            print("🎭 Available genres:")
            for i, (name, _) in enumerate(CATEGORIES.items(), start=1):
                print(f"{i}. {name}")
            genre_choice = input("🎯 Choose genre number: ").strip()
            try:
                index = int(genre_choice) - 1
                genre_name = list(CATEGORIES.keys())[index]
                genre_url = CATEGORIES[genre_name].format(region=region)
                process_extraction(driver, f"genre_{genre_name.lower()}", genre_url)
            except (ValueError, IndexError):
                print("❌ Invalid genre choice.")
        elif choice == "4":
            print("👋 Exiting scraper. Goodbye!")
            break
        else:
            print("❌ Invalid input. Try again.")

    driver.quit()

if __name__ == "__main__":
    main()
