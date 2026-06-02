from src.ai.gemini_client import ask_gemini

def score_opportunity(
    ticker,
    why,
    quote
):

    prompt = f"""
You are an early-opportunity stock analyst.

Evaluate this idea.

Ticker: {ticker}

News relevance:
{why}

Current Market Context:
Price Change Today: {quote['change_pct']}%

Goal:
Find EARLY opportunities.

Penalize:
- already fully priced moves
- weak catalysts

Reward:
- emerging catalysts
- Trump/policy relevance
- not fully priced stories

Respond ONLY:

Ticker:
Conviction: LOW/MEDIUM/HIGH
Opportunity Stage: EARLY/MOVING/LATE
Why:
FollowUp: YES/NO
"""

    return ask_gemini(prompt)
