from google import genai

from src.config import GEMINI_API_KEY
from src.ai.gemini_usage import increment_request
from src.ai.guardrails import can_use_gemini

client = genai.Client(
    api_key=GEMINI_API_KEY
)

PRIMARY_MODEL = "gemini-3.1-flash-lite"

def ask_gemini(prompt):

    if not can_use_gemini():

        print(
            "Gemini daily limit reached"
        )

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

                if (
                    hasattr(part, "text")
                    and part.text
                ):
                    parts.append(part.text)

        text = "\n".join(
            parts
        ).strip()

        if text:
            increment_request()

        return text

    except Exception as e:

        print(
            "Gemini failed:",
            e
        )

        return None
