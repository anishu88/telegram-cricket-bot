import requests
import time

# ================= CONFIG =================
BOT_TOKEN = "8791230210:AAGGBf2fzHWI4B8aECe4eeelntIj8N9pEy4"
CHANNEL_ID = "@daddyscricketline"

sent = set()

# ================= TELEGRAM =================
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHANNEL_ID, "text": msg})
    except:
        pass

# ================= LIVE MATCHES =================
def get_matches():
    url = "https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current?lang=en&latest=true"
    try:
        return requests.get(url, timeout=10).json()
    except:
        return None

# ================= MATCH IDS =================
def get_match_ids(data):
    ids = []
    try:
        matches = data.get("content", {}).get("matches", [])
        for m in matches:
            ids.append(m.get("objectId"))
    except:
        pass
    return ids[:2]

# ================= COMMENTARY =================
def get_commentary(mid):
    url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/match/details?lang=en&matchId={mid}"
    try:
        return requests.get(url, timeout=10).json()
    except:
        return None

# ================= PARSE BALLS =================
def parse_balls(data):
    balls = []

    try:
        comm = data.get("content", {}).get("commentary", [])

        for over in comm:
            for c in over.get("commentary", []):
                text = c.get("text", "")
                ts = c.get("timestamp", "")

                if text:
                    ball_id = f"{ts}-{text}"
                    balls.append((ball_id, text))

    except:
        pass

    return balls

# ================= START BOT =================
send("🏏 BALL-BY-BALL BOT STARTED (FIXED VERSION) 🚀")

while True:

    try:
        data = get_matches()

        if not data:
            time.sleep(10)
            continue

        match_ids = get_match_ids(data)

        for mid in match_ids:

            comm = get_commentary(mid)

            if not comm:
                continue

            balls = parse_balls(comm)

            for bid, text in balls:

                if bid not in sent:

                    sent.add(bid)

                    send(f"🏏 BALL UPDATE\n\n{text}")

        time.sleep(8)

    except Exception as e:
        print("error:", e)
        time.sleep(10)
