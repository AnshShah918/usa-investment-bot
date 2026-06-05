from src.news.news_collector import get_news
from src.news.policy_filter import filter_policy_news
from src.intelligence.stock_mapper import discover_stocks
from src.market.market_context import get_quote
from src.ai.fusion_engine import run_fusion
from src.alerts.router import route_alert
from src.collectors.politician_scraper import get_politician_trades
from src.config_politicians import HIGH_IMPACT_POLITICIANS
from src.db.trade_db import init_db


def run_scan():

    init_db()

    print("\nCollecting news...")

    news = get_news()

    policy_news = filter_policy_news(news)

    print("Policy news:", len(policy_news))

    stock_candidates = discover_stocks(policy_news)

    validated = []

    for ticker, score in stock_candidates:

        quote = get_quote(ticker)

        if quote:

            validated.append({
                "ticker": ticker,
                "theme_score": score,
                "change_pct": quote["change_pct"]
            })

    headlines = [n["title"] for n in policy_news]

    print("\nFetching politician trades...")

    pol_lines = []

    for name, slug in HIGH_IMPACT_POLITICIANS.items():

        try:

            trades = get_politician_trades(slug)

            for t in trades[:2]:

                pol_lines.append(
                    f"{t['politician']} {t['transaction_type']} {t['ticker']}"
                )

        except Exception as e:

            print(f"Skipping {name}:", e)

    politician_summary = (
        "\n".join(pol_lines)
        if pol_lines
        else "No recent politician trades found."
    )

    print("Politician signals:", len(pol_lines))

    result = run_fusion(
        headlines,
        politician_summary,
        validated
    )

    print("\nFINAL INTELLIGENCE\n")
    print(result)

    route_alert(result)

    return result
