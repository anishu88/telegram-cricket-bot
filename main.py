import requests
import time
import os
from datetime import datetime

BOT_TOKEN = os.getenv("8791230210:AAGGBf2fzHWI4B8aECe4eeelntIj8N9pEy4")
CHANNEL_ID = os.getenv("@daddyscricketline")

sent_scores = set()
last_update_time = {}

def send_message(msg):
    if not BOT_TOKEN or not CHANNEL_ID:
        print("Missing env vars")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(url, data={
            "chat_id": CHANNEL_ID, 
            "text": msg,
            "parse_mode": "HTML"
        }, timeout=8)
        return response.json().get("ok", False)
    except:
        return False

def get_live_matches():
    url = "https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current?lang=en&latest=true"
    try:
        resp = requests.get(url, timeout=8)
        return resp.json()
    except:
        return None

def get_scorecard(match_id):
    url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/match/scorecard/{match_id}?lang=en"
    try:
        resp = requests.get(url, timeout=8)
        return resp.json()
    except:
        return None

def parse_ball_by_ball(match):
    try:
        match_id = str(match.get("objectId"))
        team1 = match.get("team1", {})
        team2 = match.get("team2", {})
        
        scorecard = get_scorecard(match_id)
        if not scorecard:
            return None
        
        t1_score = f"{team1.get('score', 0)}/{team1.get('wickets', 0)}"
        t2_score = f"{team2.get('score', 0)}/{team2.get('wickets', 0)}"
        
        title = match.get("name", "LIVE")
        status = match.get("statusText", "LIVE")
        
        innings = scorecard.get("content", {}).get("innings", [])
        current_batting = ""
        current_bowling = ""
        
        if innings:
            latest_innings = innings[0]
            batting_team = latest_innings.get("battingTeam", {})
            
            batsmen = latest_innings.get("batting", [])
            bat1, bat2 = "", ""
            if len(batsmen) >= 2:
                bat1_data = batsmen[0].get('batsman', {})
                bat2_data = batsmen[1].get('batsman', {})
                bat1 = f"{bat1_data.get('name', '')[:15]}: {batsmen[0].get('runs',0)}({batsmen[0].get('ballsFaced',0)})"
                bat2 = f"{bat2_data.get('name', '')[:15]}: {batsmen[1].get('runs',0)}({batsmen[1].get('ballsFaced',0)})"
            
            bowlers = latest_innings.get("bowling", [])
            bowler = ""
            if bowlers:
                bwl_data = bowlers[0].get('bowler', {})
                bowler = f"{bwl_data.get('name', '')[:15]}: {bowlers[0].get('overs',0)}-{bowlers[0].get('runs',0)}-{bowlers[0].get('wickets',0)}"
            
            current_batting = f"{batting_team.get('shortName', '')}\n{bat1}\n{bat2}"
            current_bowling = f"{bowler}"
        
        msg = f"""<b>{title}</b>
<b>{status}</b>

<b>{team1.get('team', {}).get('shortName', 'Team1')}</b>: {t1_score}
<b>{team2.get('team', {}).get('shortName', 'Team2')}</b>: {t2_score}

<b>{current_batting}</b>

{current_bowling}

<code>{datetime.now().strftime('%H:%M:%S')}</code>"""
        
        state_key = f"{match_id}_{t1_score}_{t2_score}"
        
        return {
            "msg": msg,
            "key": state_key,
            "match_id": match_id
        }
        
    except:
        return None

def main():
    print("Bot starting...")
    send_message("Ball-by-Ball Bot Started")
    
    while True:
        try:
            now = time.time()
            
            matches_data = get_live_matches()
            if not matches_data:
                time.sleep(10)
                continue
            
            matches = matches_data.get("content", {}).get("matches", [])
            
            for match in matches:
                result = parse_ball_by_ball(match)
                
                if result:
                    match_id = result["match_id"]
                    
                    if result["key"] not in sent_scores or (now - last_update_time.get(match_id, 0)) > 60:
                        if send_message(result["msg"]):
                            sent_scores.add(result["key"])
                            last_update_time[match_id] = now
                            print(f"Updated: {match_id}")
            
            time.sleep(10)
            
        except KeyboardInterrupt:
            break
        except:
            time.sleep(10)

if __name__ == "__main__":
    main(
