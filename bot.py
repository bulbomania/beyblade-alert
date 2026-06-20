import requests
from bs4 import BeautifulSoup
import json
import os

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.amazon.co.jp/s?k=beyblade+x&crid=33LWC80LC0AK6&sprefix=%2Caps%2C232&ref=nb_sb_noss_2"

DB_FILE = "seen.json"

def send_message(text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

def load_seen():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            return set(json.load(f))
    return set()

def save_seen(data):
    with open(DB_FILE, "w") as f:
        json.dump(list(data), f)

r = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

soup = BeautifulSoup(r.text, "html.parser")

seen = load_seen()

current = set()

for item in soup.select("[data-asin]"):
    asin = item.get("data-asin", "").strip()

    if not asin:
        continue

    title = item.select_one("h2 span")

    if not title:
        continue

    title = title.get_text(strip=True)

    current.add(asin)

    if asin not in seen:
        send_message(
            f"🆕 Nuovo prodotto Beyblade X:\n\n{title}"
        )

seen.update(current)
save_seen(seen)
