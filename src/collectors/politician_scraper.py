import requests
import re
import json

headers = {
    "User-Agent": "Mozilla/5.0"
}

BASE_URL = "https://www.quiverquant.com"

def get_politician_trades(slug):
    url = f"{BASE_URL}/congresstrading/politician/{slug}"

    r = requests.get(url, headers=headers, timeout=30)

    if r.status_code != 200:
        print("Failed:", r.status_code)
        return []

    html = r.text

    match = re.search(
        r'let tradeData = (\[.*?\]);',
        html,
        re.DOTALL
    )

    if not match:
        print("No tradeData found")
        return []

    raw = match.group(1)

    try:
        data = json.loads(raw)

        trades = []

        for t in data:
            trade = {
                "trade_id": t[7],
                "ticker": t[0],
                "transaction_type": t[1],
                "filed_date": t[2],
                "trade_date": t[3],
                "description": t[4],
                "excess_return": t[5],
                "politician": t[6],
                "asset_name": t[8],
                "asset_type": t[9],
                "amount_range": t[10],
                "party": t[12],
                "sector": t[13],
                "estimated_value": t[14]
            }

            trades.append(trade)

        return trades

    except Exception as e:
        print("JSON parse error:", e)
        return []
