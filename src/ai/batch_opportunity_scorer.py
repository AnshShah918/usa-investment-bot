from src.ai.gemini_client import ask_gemini

def score_batch(stocks):

    stock_text = ""

    for s in stocks:

        stock_text += f"""
Ticker: {s['ticker']}
Why: {s['why']}
Daily Move: {s['change_pct']}%
"""

    prompt = f"""
You are an EARLY opportunity stock analyst.

Evaluate these stocks.

Goal:
Find early ideas.

Penalize:
- already fully priced
- weak catalysts
- hype

Reward:
- emerging Trump/news catalysts
- underpriced themes
- actionable ideas

{stock_text}

Respond ONLY:

1.
Ticker:
Conviction:
Stage: EARLY/MOVING/LATE
Why:
FollowUp:

2.
Ticker:
Conviction:
Stage:
Why:
FollowUp:

3.
Ticker:
Conviction:
Stage:
Why:
FollowUp:
"""

    return ask_gemini(prompt)
