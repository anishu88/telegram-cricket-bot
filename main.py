import requests
import time

BOT_TOKEN = "8791230210:AAGHr_mGA03UJPsxmPX8T7VQIZ8NdQpM560"
CHANNEL_ID = "@bpnB2V8M3ODM1"

def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    data = {
        "chat_id": CHANNEL_ID,
        "text": msg
    }

    requests.post(url, data=data)

last_message = ""

while True:
    try:
        api = "https://api.cricapi.com/v1/currentMatches?apikey=demo&offset=0"
        
        response = requests.get(api).json()

        if "data" in response:

            match = response["data"][0]

            teams = " vs ".join(match["teams"])

            score_text = ""

            if "score" in match:

                for s in match["score"]:

                    score_text += f"{s['inning']} - {s['r']}/{s['w']} ({s['o']} ov)\n"

            message = f"🏏 LIVE SCORE UPDATE\n\n{teams}\n\n{score_text}"


            if message != last_message:
                send_message(message)
                last_message = message

        time.sleep(60)

    except Exception as e:
        print(e)
        time.sleep(60)
