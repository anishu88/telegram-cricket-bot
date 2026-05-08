import requests
import time

BOT_TOKEN = "8791230210:AAGGBf2fzHWI4B8aECe4eeelntIj8N9pEy4"
CHANNEL_ID = "@daddyscricketline"

RAPID_API_KEY = "3feaa2c6e0mshb44e29d5d69fc27p109f2fjsne898ba876593"

headers = {
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
    "x-rapidapi-key": RAPID_API_KEY
}

def send_message(msg):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHANNEL_ID,
        "text": msg
    }

    requests.post(url, data=data)

last_message = ""

send_message("🏏 Live Cricket Bot Started ✅")

while True:

    try:

        api_url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

        response = requests.get(api_url, headers=headers)

        data = response.json()

        message = "🏏 LIVE CRICKET SCORES\n\n"

        for match_type in data["typeMatches"]:

            for series in match_type["seriesMatches"]:

                if "seriesAdWrapper" in series:

                    matches = series["seriesAdWrapper"]["matches"]

                    for match in matches[:2]:

                        info = match["matchInfo"]

                        team1 = info["team1"]["teamName"]
                        team2 = info["team2"]["teamName"]

                        status = info["status"]

                        message += f"{team1} vs {team2}\n"
                        message += f"{status}\n\n"

        if message != last_message:

            send_message(message)

            last_message = message

        time.sleep(120)

    except Exception as e:

        print(e)

        time.sleep(120)
