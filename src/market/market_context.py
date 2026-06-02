import requests

from src.config import FINNHUB_API_KEY

BASE_URL = "https://finnhub.io/api/v1/quote"

def get_quote(symbol):

    url = (
        f"{BASE_URL}"
        f"?symbol={symbol}"
        f"&token={FINNHUB_API_KEY}"
    )

    r = requests.get(url, timeout=30)

    if r.status_code != 200:
        return None

    data = r.json()

    return {
        "current": data.get("c"),
        "change_pct": data.get("dp"),
        "high": data.get("h"),
        "low": data.get("l")
    }
