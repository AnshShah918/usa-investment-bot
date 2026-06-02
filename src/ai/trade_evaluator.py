from datetime import datetime
from src.ai.gemini_client import ask_gemini

def evaluate_trade(trade):

    trade_dt = datetime.fromisoformat(
        trade["trade_date"]
    )

    filed_dt = datetime.fromisoformat(
        trade["filed_date"]
    )

    delay = (filed_dt - trade_dt).days

    prompt = f"""
You are a stock intelligence analyst.

Evaluate this politician trade.

Politician: {trade['politician']}
Ticker: {trade['ticker']}
Transaction: {trade['transaction_type']}
Sector: {trade['sector']}
Estimated Value: {trade['estimated_value']}
Trade Date: {trade['trade_date']}
Filed Date: {trade['filed_date']}
Disclosure Delay: {delay} days
Asset: {trade['asset_name']}

Consider disclosure delay.

If delay is large, lower urgency.

Respond only:

Importance: LOW/MEDIUM/HIGH
Urgency: LOW/MEDIUM/HIGH
Reason: one short sentence
FollowUp: YES/NO
"""

    return ask_gemini(prompt)
