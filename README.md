# 🎬 Amazon Prime Video Scraper (by Mike | DRMLab.io)

An intelligent and interactive Python scraper for [https://www.primevideo.com](https://www.primevideo.com), designed to extract movie and series links via storefront, genre, or keyword search.

---

## 🚀 Features

### 🎛️ Menu Options
- `1️⃣` Extract from the main storefront
- `2️⃣` Search by keyword (manual or random)
- `3️⃣` Browse by genre (Action, Comedy, Drama, etc.)
- `4️⃣` Exit

---

### 🧠 Built-in Intelligence
- ✅ Duplicate link filtering using `seen_links_prime.txt`
- 🎬 Shows movie title (`alt`, `title`, or inner text)
- 📜 Full page scroll support (lazy loading)
- 💾 Saves links in `output_prime/` folder (10+ per file)
- 🕐 Timestamped filenames (e.g. `prime_search_war_20250516_184030.txt`)
- 📊 Shows number of new links and skipped duplicates
- 🧾 Writes to `log.txt` after each scan

---

## 📦 Requirements
- Python 3.8+
- Google Chrome (installed)
- Selenium
- WebDriver Manager

```bash
pip install selenium webdriver-manager

🔮 Planned Features
	•	🔐 Profile selection support
	•	🍪 Cookie-based auto-login
	•	📥 Integration with vt dl for automated downloads
	•	📈 More metadata per movie (poster, description, etc.)
    
