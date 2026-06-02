from src.ai.gemini_client import ask_gemini

def run_fusion(
    headlines,
    politician_summary,
    stocks
):

    news_text = "\n".join(
        [f"- {h}" for h in headlines[:10]]
    )

    stock_text = ""

    for s in stocks:

        stock_text += f"""
Ticker: {s['ticker']}
Move: {s['change_pct']}%
Why: {s['why']}
"""

    prompt = f"""
You are an EARLY opportunity market analyst.

Goal:
Find emerging opportunities.

NEWS:
{news_text}

POLITICIAN SIGNALS:
{politician_summary}

MARKET:
{stock_text}

Reward:
- emerging themes
- Trump/policy relevance
- politician overlap
- not fully priced

Penalize:
- crowded trades
- hype
- weak narratives

Return ONLY TOP 5 opportunities.

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

4.
Ticker:
Conviction:
Stage:
Why:
FollowUp:

5.
Ticker:
Conviction:
Stage:
Why:
FollowUp:
"""

    return ask_gemini(prompt)
