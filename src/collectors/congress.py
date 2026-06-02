import requests

URL = "https://senatestockwatcher.com/api/trades?pageSize=10&page=0"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_congress_trades():
    try:
        response = requests.get(URL, headers=headers, timeout=30)

        if response.status_code != 200:
            print("Fetch failed:", response.status_code)
            return []

        return response.json()

    except Exception as e:
        print("Error:", e)
        return []
