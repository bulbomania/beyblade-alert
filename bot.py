import os
import requests

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

print("CHAT_ID =", CHAT_ID)

r = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={
        "chat_id": CHAT_ID,
        "text": "✅ Test GitHub Actions"
    }
)

print("STATUS:", r.status_code)
print("RESPONSE:", r.text)
