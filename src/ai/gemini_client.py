from datetime import date
from google import genai
import os

from src.config import GEMINI_API_KEY
from src.ai.gemini_usage import increment_request, reset_usage, get_usage
from src.ai.guardrails import can_use_gemini

client = genai.Client(
    api_key=GEMINI_API_KEY
)

PRIMARY_MODEL = "gemini-2.0-flash-lite"

USAGE_DATE_FILE = "gemini_usage_date.txt"

def _auto_reset_if_new_day():
    today = str(date.today())
    if os.path.exists(USAGE_DATE_FILE):
        with open(USAGE_DATE_FILE) as f:
            if f.read().strip() == today:
                return
    reset_usage()
    with open(USAGE_DATE_FILE, "w") as f:
        f.write(today)

def ask_gemini(prompt):

    _auto_reset_if_new_day()

    if not can_use_gemini():
        print("Gemini daily limit reached")
        return None

    try:
        response = client.models.generate_content(
            model=PRIMARY_MODEL,
            contents=prompt
        )

        parts = []

        if (
            hasattr(response, "candidates")
            and response.candidates
        ):
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    parts.append(part.text)

        text = "\n".join(parts).strip()

        if text:
            increment_request()

        return text

    except Exception as e:
        print("Gemini failed:", e)
        return None
