from datetime import date
from google import genai
import os
import time

from src.config import GEMINI_API_KEY
from src.ai.gemini_usage import increment_request, reset_usage, get_usage
from src.ai.guardrails import can_use_gemini

client = genai.Client(
    api_key=GEMINI_API_KEY
)

PRIMARY_MODEL = "gemini-2.5-flash"

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

def ask_gemini(prompt, retries=3, base_delay=60):

    _auto_reset_if_new_day()

    if not can_use_gemini():
        print("Gemini daily limit reached")
        return None

    for attempt in range(retries):
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
            err = str(e)
            if "429" in err and attempt < retries - 1:
                wait = base_delay * (attempt + 1)
                print(f"Gemini 429 - waiting {wait}s before retry {attempt + 1}/{retries - 1}...")
                time.sleep(wait)
            else:
                print("Gemini failed:", e)
                return None

    return None
