import requests

URL = "https://senatestockwatcher.com/api/v1"

def get_congress_trades():
    try:
        response = requests.get(URL, timeout=30)

        if response.status_code != 200:
            print("Fetch failed:", response.status_code)
            print(response.text)
            return []

        return response.json()

    except Exception as e:
        print("Error:", e)
        return []
