import re
from src.ai.gemini_client import ask_gemini

def discover_stocks(news_items):

    headlines = "\n".join(
        [
            f"- {n['title']}"
            for n in news_items
        ]
    )

    prompt = f"""
You are a US political-market analyst.

These are POLICY and GOVERNMENT headlines.

{headlines}

IMPORTANT:

Do NOT suggest random stocks.

ONLY identify companies or sectors
DIRECTLY impacted by:

- Pentagon
- Trump
- Congress
- tariffs
- sanctions
- defense
- trade policy
- executive action

Find:

1 direct beneficiaries
2 indirect beneficiaries
3 negatively impacted firms

Maximum 5 ideas.

Respond ONLY:

1.
Ticker:
Policy Link:
Why:

2.
Ticker:
Policy Link:
Why:

3.
Ticker:
Policy Link:
Why:

4.
Ticker:
Policy Link:
Why:

5.
Ticker:
Policy Link:
Why:
"""

    result = ask_gemini(
        prompt
    )

    if not result:
        return []

    print(
        "\nPOLICY STOCK MAP\n"
    )
    print(result)

    stocks = []

    ticker_matches = re.findall(
        r"Ticker:\s*\**([A-Z\.]+)\**",
        result
    )

    why_matches = re.findall(
        r"Why:\s*(.*)",
        result
    )

    for i, ticker in enumerate(
        ticker_matches
    ):

        stocks.append({
            "ticker": ticker,
            "why": (
                why_matches[i]
                if i < len(why_matches)
                else ""
            )
        })

    return stocks
