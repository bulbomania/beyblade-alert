import requests
from bs4 import BeautifulSoup
import json
import os

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.amazon.co.jp/s?k=beyblade+x&crid=33LWC80LC0AK6&sprefix=%2Caps%2C232&ref=nb_sb_noss_2"

DB_FILE = "seen.json"

def send_message(text):
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

    print("TELEGRAM STATUS:", r.status_code)

def load_seen():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            return set(json.load(f))
    return set()

def save_seen(data):
    with open(DB_FILE, "w") as f:
        json.dump(list(data), f)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

r = requests.get(
    URL,
    headers=headers,
    timeout=30
)

print("AMAZON STATUS:", r.status_code)
print("URL FINALE:", r.url)

print("AMAZON STATUS:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

items = soup.select("[data-asin]")

print("PRODOTTI TROVATI:", len(items))

seen = load_seen()
current = set()

for item in items:
    asin = item.get("data-asin", "").strip()

    print("ASIN:", asin)

    if not asin:
        continue

    title = item.select_one("h2 span")

    if not title:
        continue

    title = title.get_text(strip=True)

    print("TITOLO:", title)

    current.add(asin)

    if asin not in seen:
        print("NUOVO PRODOTTO:", title)

        send_message(
            f"🆕 Nuovo prodotto Beyblade X:\n\n{title}"
        )

seen.update(current)
save_seen(seen)

print("FINE")
