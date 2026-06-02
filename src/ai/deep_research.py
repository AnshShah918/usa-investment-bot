from src.ai.gemini_client import ask_gemini
from src.market.market_context import get_quote

def deep_dive(ticker):

    quote = get_quote(ticker)

    prompt = f"""
You are a professional market analyst.

Analyze ticker:

{ticker}

Market context:

{quote}

Explain:

1 Why this stock matters
2 Bull case
3 Bear case
4 Key catalysts
5 What to monitor next

Respond clearly and practically.
"""

    return ask_gemini(prompt)
