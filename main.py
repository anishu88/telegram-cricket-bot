import requests

BOT_TOKEN = "8791230210:AAGGBf2fzHWI4B8aECe4eeelntIj8N9pEy4"
CHANNEL_ID = "@daddyscricketline"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

data = {
    "chat_id": CHANNEL_ID,
    "text": "Bot Started Successfully ✅"
}

requests.post(url, data=data)

print("done")
