import requests
import time
import sqlite3

BOT_TOKEN = "8791230210:AAGGBf2fzHWI4B8aECe4eeelntIj8N9pEy4"
CHANNEL_ID = "@daddyscricketline"

RAPID_API_KEY = "3feaa2c6e0mshb44e29d5d69fc27p109f2fjsne898ba876593"

headers = {
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
    "x-rapidapi-key": RAPID_API_KEY
}

conn = sqlite3.connect("ballbot.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS sent (id TEXT PRIMARY KEY)")
conn.commit()


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHANNEL_ID, "text": msg})


def get_live_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
    return requests.get(url, headers=headers).json()


def get_match_ids(data):
    ids = []

    for t in data.get("typeMatches", []):
        for s in t.get("seriesMatches", []):
            if "seriesAdWrapper" in s:
                for m in s["seriesAdWrapper"]["matches"]:
                    ids.append(m["matchInfo"]["matchId"])

    return ids  # ALL matches (IPL + others)


def get_commentary(mid):
    try:
        url = f"https://cricbuzz-cricket.p.rapidapi.com/matches/v1/commentary/{mid}"
        return requests.get(url, headers=headers, timeout=10).json()
    except:
        return None


def is_sent(eid):
    cur.execute("SELECT 1 FROM sent WHERE id=?", (eid,))
    return cur.fetchone() is not None


def mark(eid):
    cur.execute("INSERT OR IGNORE INTO sent (id) VALUES (?)", (eid,))
    conn.commit()


def parse(data):
    events = []

    if not data:
        return events

    for c in data.get("commentary", []):
        text = c.get("commText", "")
        over = c.get("overNum", "")
        ball = c.get("ballNum", "")

        if text:
            eid = f"{over}-{ball}-{text}"
            events.append((eid, text))

    return events


send("🏏 GLOBAL BALL-BY-BALL BOT STARTED (IPL + ALL MATCHES) 🚀")

while True:

    try:
        live = get_live_matches()

        match_ids = get_match_ids(live)

        for mid in match_ids:

            comm = get_commentary(mid)
            balls = parse(comm)

            for eid, text in balls:

                if not is_sent(eid):

                    mark(eid)

                    send(f"🏏 BALL UPDATE\n\n{text}")

        time.sleep(10)

    except Exception as e:
        print(e)
        time.sleep(15)
