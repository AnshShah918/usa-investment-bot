import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

FINNHUB_API_KEY = os.getenv(
    "FINNHUB_API_KEY"
)

TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)

TELEGRAM_CHAT_IDS = [
    c.strip()
    for c in os.getenv(
        "TELEGRAM_CHAT_IDS",
        ""
    ).split(",")
    if c.strip()
]
