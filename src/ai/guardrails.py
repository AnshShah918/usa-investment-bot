from src.ai.gemini_usage import get_usage

DAILY_LIMIT = 200

def can_use_gemini():

    usage = get_usage()

    return usage < DAILY_LIMIT
