import requests

from src.config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_IDS
)

def send_telegram(message):

    url = (
        f"https://api.telegram.org/bot"
        f"{TELEGRAM_BOT_TOKEN}/sendMessage"
    )

    for chat_id in TELEGRAM_CHAT_IDS:

        payload = {
            "chat_id": chat_id,
            "text": message
        }

        r = requests.post(
            url,
            json=payload,
            timeout=30
        )

        print(
            "Telegram",
            chat_id,
            r.status_code
        )
