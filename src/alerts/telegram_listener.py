import requests

from src.config import TELEGRAM_BOT_TOKEN

BASE_URL = (
    f"https://api.telegram.org/bot"
    f"{TELEGRAM_BOT_TOKEN}"
)

def get_updates(offset=None):

    url = f"{BASE_URL}/getUpdates"

    params = {
        "timeout": 10
    }

    if offset:
        params["offset"] = offset

    r = requests.get(
        url,
        params=params,
        timeout=30
    )

    return r.json()
