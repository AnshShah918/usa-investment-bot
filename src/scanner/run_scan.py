from src.news.news_collector import get_news
from src.news.policy_filter import filter_policy_news
from src.news.stock_mapper import discover_stocks
from src.market.market_context import get_quote
from src.ai.fusion_engine import run_fusion
from src.alerts.router import route_alert

def run_scan():

    print(
        "\nCollecting news..."
    )

    news = get_news()

    policy_news = filter_policy_news(
        news
    )

    print(
        "Policy news:",
        len(policy_news)
    )

    stocks = discover_stocks(
        policy_news
    )

    validated = []

    for s in stocks:

        quote = get_quote(
            s["ticker"]
        )

        if quote:

            validated.append({
                "ticker": s["ticker"],
                "why": s["why"],
                "change_pct": quote["change_pct"]
            })

    headlines = [
        n["title"]
        for n in policy_news
    ]

    politician_summary = """
Congress trades monitored.
Political relevance prioritized.
"""

    result = run_fusion(
        headlines,
        politician_summary,
        validated
    )

    print(
        "\nFINAL INTELLIGENCE\n"
    )

    print(result)

    route_alert(
        result
    )

    return result
