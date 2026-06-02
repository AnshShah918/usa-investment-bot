from src.ai.gemini_client import ask_gemini
from src.market.market_context import get_quote

def evaluate_news(news_items):

    headlines = "\n".join(
        [f"- {n['title']}" for n in news_items[:10]]
    )

    prompt = f"""
You are a macro, Trump-policy and stock analyst.

Analyze these headlines.

{headlines}

Task:

1 Identify major themes.
2 Explain Trump/policy impact.
3 Identify ONLY top 3 highest relevance US stocks.
4 No filler names.
5 Focus on strongest links.

Respond ONLY:

Themes:
- theme
- theme

Trump Impact:
short explanation

Top Stocks:

1.
Ticker:
Why:

2.
Ticker:
Why:

3.
Ticker:
Why:
"""

    first_pass = ask_gemini(prompt)

    if not first_pass:
        return None

    print(first_pass)

    return first_pass
