import requests
import time
import sqlite3

# ================= CONFIG =================
BOT_TOKEN = "8791230210:AAGGBf2fzHWI4B8aECe4eeelntIj8N9pEy4"
CHANNEL_ID = "@daddyscricketline"
RAPID_API_KEY = "3feaa2c6e0mshb44e29d5d69fc27p109f2fjsne898ba876593"

headers = {
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
    "x-rapidapi-key": RAPID_API_KEY
}

# ================= DATABASE =================
conn = sqlite3.connect("pro_cricket.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS sent (
    id TEXT PRIMARY KEY
)
""")
conn.commit()

# ================= TELEGRAM =================
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHANNEL_ID,
        "text": msg
    })

# ================= LIVE MATCHES =================
def get_live_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
    try:
        return requests.get(url, headers=headers, timeout=10).json()
    except:
        return None

# ================= MATCH IDS =================
def get_match_ids(data):
    ids = []

    try:
        for t in data.get("typeMatches", []):
            for s in t.get("seriesMatches", []):
                if "seriesAdWrapper" in s:
                    for m in s["seriesAdWrapper"]["matches"]:
                        ids.append(m["matchInfo"]["matchId"])
    except:
        pass

    return ids[:3]

# ================= COMMENTARY =================
def get_commentary(mid):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/matches/v1/commentary/{mid}"
    try:
        return requests.get(url, headers=headers, timeout=10).json()
    except:
        return None

# ================= PARSE EVENTS =================
def parse_events(data):
    events = []

    if not data:
        return events

    try:
        for c in data.get("commentary", []):
            text = c.get("commText", "")
            over = c.get("overNum", "")
            ball = c.get("ballNum", "")

            if not text:
                continue

            ball_id = f"{over}-{ball}-{text}"

            # 🎯 EVENT TYPE DETECTION
            event_type = "BALL"

            t = text.lower()
            if "out" in t or "wicket" in t:
                event_type = "WICKET"
            elif "six" in t:
                event_type = "SIX"
            elif "four" in t:
                event_type = "FOUR"

            msg = f"🏏 {event_type}\n\n{text}"

            events.append((ball_id, msg))

    except:
        pass

    return events

# ================= DUPLICATE CHECK =================
def sent(ball_id):
    cur.execute("SELECT 1 FROM sent WHERE id=?", (ball_id,))
    return cur.fetchone() is not None

def mark(ball_id):
    cur.execute("INSERT OR IGNORE INTO sent (id) VALUES (?)", (ball_id,))
    conn.commit()

# ================= START BOT =================
send("🏏 PRO CRICKET BROADCAST BOT STARTED 🚀")

while True:

    try:
        live = get_live_matches()

        if not live:
            time.sleep(8)
            continue

        match_ids = get_match_ids(live)

        for mid in match_ids:

            data = get_commentary(mid)
            events = parse_events(data)

            for eid, msg in events:

                if not sent(eid):

                    mark(eid)

                    send(msg)

        time.sleep(8)

    except Exception as e:
        print("error:", e)
        time.sleep(10)
