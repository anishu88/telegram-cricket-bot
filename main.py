import requests
import time
import os
from datetime import datetime

BOT_TOKEN = os.getenv("8791230210:AAF1ktE0w1yfvu8HB8EwjBCQXLhV1LZbtNk")
CHANNEL_ID = os.getenv("@daddyscricketline")

sent_scores = set()

def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={
            "chat_id": CHANNEL_ID,
            "text": msg,
            "parse_mode": "HTML"
        }, timeout=5)
        return True
    except:
        return False

def get_live_matches():
    url = "https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current?lang=en&latest=true"
    try:
        return requests.get(url, timeout=5).json()
    except:
        return None

def get_scorecard(match_id):
    url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/match/scorecard/{match_id}?lang=en"
    try:
        return requests.get(url, timeout=5).json()
    except:
        return None

def format_match(match):
    try:
        match_id = str(match.get("objectId"))
        team1 = match.get("team1", {})
        team2 = match.get("team2", {})
        
        scorecard = get_scorecard(match_id)
        
        t1_name = team1.get("team", {}).get("shortName", "Team1")
        t2_name = team2.get("team", {}).get("shortName", "Team2")
        t1_score = f"{team1.get('score', 0)}/{team1.get('wickets', 0)}"
        t2_score = f"{team2.get('score', 0)}/{team2.get('wickets', 0)}"
        
        title = match.get("name", "LIVE MATCH")
        
        msg = f"<b>{title}</b>\n\n"
        msg += f"<b>{t1_name}</b>: {t1_score}\n"
        msg += f"<b>{t2_name}</b>: {t2_score}\n\n"
        msg += f"<code>{datetime.now().strftime('%H:%M:%S')}</code>"
        
        key = f"{match_id}_{t1_score}_{t2_score}"
        return msg, key, match_id
    except:
        return None, None, None

print("Starting bot...")
send_message("Cricket Bot Started")

while True:
    try:
        data = get_live_matches()
        if data:
            matches = data.get("content", {}).get("matches", [])
            
            for match in matches:
                result = format_match(match)
                if result[0] and result[1] not in sent_scores:
                    send_message(result[0])
                    sent_scores.add(result[1])
        
        time.sleep(10)
        
    except:
        time.sleep(10)
