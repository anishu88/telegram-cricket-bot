mport requests
import time
import os

BOT_TOKEN = os.getenv("8791230210:AAGGBf2fzHWI4B8aECe4eeelntIj8N9pEy4")
CHANNEL_ID = os.getenv("@daddyscricketline")

sent = set()

# ================= TELEGRAM =================
def send(msg):
    if not BOT_TOKEN or not CHANNEL_ID:
        print("Missing env variables")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHANNEL_ID, "text": msg})
    except Exception as e:
        print("Telegram error:", e)

# ================= ESPN LIVE DATA =================
def get_matches():
    url = "https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current?lang=en&latest=true"
    try:
        return requests.get(url, timeout=10).json()
    except:
        return None

# ================= PARSE MATCHES =================
def parse_matches(data):
    results = []

    if not data:
        return results

    try:
        matches = data.get("content", {}).get("matches", [])

        for m in matches:
            mid = str(m.get("objectId"))
            name = m.get("slug", "Match")
            status = m.get("status", "LIVE")

            msg = f"🏏 {name}\n📌 {status}"
            results.append((mid, msg))

    except Exception as e:
        print("parse error:", e)

    return results

# ================= START =================
print("BOT STARTING...")

send("🏏 Cricket Bot Started Successfully 🚀")

while True:

    try:
        data = get_matches()
        matches = parse_matches(data)

        for mid, msg in matches:

            if mid not in sent:
                sent.add(mid)
                send(msg)

        time.sleep(10)

    except Exception as e:
        print("loop error:", e)
        time.sleep(10)
