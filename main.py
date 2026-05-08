import requests
import time
import os

BOT_TOKEN = os.getenv("8791230210:AAH3h1EgwJFCFA7k1lEW_tkFxDeZ9r2_MaM")
CHANNEL_ID = os.getenv("@daddyscricketline")

sent = set()

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHANNEL_ID, "text": msg})

# ================= MATCH LIST =================
def get_matches():
    url = "https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current?lang=en&latest=true"
    return requests.get(url).json()

# ================= SCORE DETAILS (IMPORTANT FIX) =================
def get_score(mid):
    url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/match/details?lang=en&matchId={mid}"
    return requests.get(url).json()

# ================= PARSE SCORE =================
def parse_score(data):
    try:
        match = data.get("content", {}).get("match", {})

        teams = match.get("teams", [])
        status = match.get("status", "LIVE")

        score_text = ""

        for t in match.get("innings", []):
            team = t.get("team", {}).get("name", "")
            runs = t.get("runs", 0)
            wickets = t.get("wickets", 0)
            overs = t.get("overs", 0)

            score_text += f"{team}: {runs}/{wickets} ({overs})\n"

        name = " vs ".join([t.get("name","") for t in teams])

        return f"🏏 {name}\n\n{score_text}\n📌 {status}"

    except:
        return None

# ================= MAIN =================
send("🏏 SCORE BOT STARTED 🚀")

while True:
    try:
        data = get_matches()
        matches = data.get("content", {}).get("matches", [])

        for m in matches:
            mid = m.get("objectId")

            if not mid:
                continue

            if mid not in sent:

                score_data = get_score(mid)
                msg = parse_score(score_data)

                if msg:
                    sent.add(mid)
                    send(msg)

        time.sleep(10)

    except Exception as e:
        print("error:", e)
        time.sleep(10)
