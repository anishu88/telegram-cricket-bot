import requests
import time

BOT_TOKEN = "8791230210:AAH3h1EgwJFCFA7k1lEW_tkFxDeZ9r2_MaM"
CHANNEL_ID = "@daddyscricketline"
RAPID_API_KEY = "3feaa2c6e0mshb44e29d5d69fc27p109f2fjsne898ba876593"

headers = {
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
    "x-rapidapi-key": RAPID_API_KEY
}

def send_message(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHANNEL_ID, "text": msg})
    except:
        pass

# ⚠️ IMPORTANT: send only once
bot_started = False

last_status_map = {}

while True:
    try:
        if not bot_started:
            send_message("🏏 Cricbuzz Live Bot Started ✅")
            bot_started = True

        api_url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

        response = requests.get(api_url, headers=headers, timeout=10)

        # 🚨 check response
        if response.status_code != 200:
            print("API ERROR:", response.text)
            time.sleep(30)
            continue

        data = response.json()

        if "typeMatches" not in data:
            print("Invalid response structure")
            time.sleep(30)
            continue

        for match_type in data.get("typeMatches", []):

            for series in match_type.get("seriesMatches", []):

                if "seriesAdWrapper" not in series:
                    continue

                matches = series["seriesAdWrapper"].get("matches", [])

                for match in matches:

                    info = match.get("matchInfo", {})

                    match_id = info.get("matchId")
                    team1 = info.get("team1", {}).get("teamName", "")
                    team2 = info.get("team2", {}).get("teamName", "")
                    status = info.get("status", "")

                    if not match_id:
                        continue

                    # only send if changed
                    if last_status_map.get(match_id) != status:

                        msg = f"""🏏 LIVE UPDATE

{team1} vs {team2}
📊 {status}
"""

                        send_message(msg)

                        last_status_map[match_id] = status

        time.sleep(30)

    except Exception as e:
        print("ERROR:", e)
        time.sleep(30)
