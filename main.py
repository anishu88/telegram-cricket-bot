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

# ================= DB (NO DUPLICATES) =================
conn = sqlite3.connect("cricket_bot.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS sent (
    id TEXT PRIMARY KEY
)
""")
conn.commit()

# ================= TELEGRAM =================
def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHANNEL_ID,
        "text": msg
    })

# ================= LIVE MATCH API =================
def get_live_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        return r.json()
    except:
        return None

# ================= SAFE PARSER =================
def parse_live_scores(data):
    messages = []

    if not data:
        return messages

    try:
        for t in data.get("typeMatches", []):
            for s in t.get("seriesMatches", []):
                if "seriesAdWrapper" in s:

                    for m in s["seriesAdWrapper"]["matches"]:

                        info = m.get("matchInfo", {})
                        score = m.get("matchScore", {})

                        team1 = info.get("team1", {}).get("teamName", "")
                        team2 = info.get("team2", {}).get("teamName", "")

                        status = info.get("status", "LIVE")

                        match_id = str(info.get("matchId"))

                        msg = f"🏏 {team1} vs {team2}\n"
                        msg += f"📊 {status}\n"

                        messages.append((match_id, msg))

    except Exception as e:
        print("parse error:", e)

    return messages

# ================= DUPLICATE CHECK =================
def already_sent(mid):
    cur.execute("SELECT 1 FROM sent WHERE id=?", (mid,))
    return cur.fetchone() is not None

def mark_sent(mid):
    cur.execute("INSERT OR IGNORE INTO sent (id) VALUES (?)", (mid,))
    conn.commit()

# ================= START BOT =================
send_message("🏏 LIVE CRICKET BOT STARTED (STABLE MODE) 🚀")

while True:

    try:
        data = get_live_matches()
        matches = parse_live_scores(data)

        for mid, msg in matches:

            if not already_sent(mid):

                mark_sent(mid)

                send_message(msg)

        time.sleep(15)

    except Exception as e:
        print("error:", e)
        time.sleep(10)
