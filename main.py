from src.news.news_collector import get_news
from src.news.stock_mapper import discover_stocks
from src.market.market_context import get_quote
from src.ai.fusion_engine import run_fusion
from src.alerts.router import route_alert
from src.alerts.telegram_listener import get_updates
from src.alerts.telegram_alert import send_telegram
from src.ai.deep_research import deep_dive
from src.alerts.help_menu import help_text

print("\nChecking Telegram...\n")

updates = get_updates()

latest_text = ""

if updates.get("result"):

    latest = updates["result"][-1]

    latest_text = latest["message"].get(
        "text",
        ""
    )

    print(
        "Telegram command:",
        latest_text
    )

    if latest_text.startswith("/help"):

        send_telegram(
            help_text()
        )

        quit()

    elif latest_text.startswith("/deep"):

        ticker = (
            latest_text
            .replace("/deep", "")
            .strip()
            .upper()
        )

        result = deep_dive(
            ticker
        )

        send_telegram(
            result
        )

        quit()

    elif latest_text.startswith("/top"):

        print(
            "Manual scan requested"
        )

print("\nCollecting news...")

news = get_news()

stocks = discover_stocks(news)

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
    for n in news
]

politician_summary = """
Politician trades monitored.
No strong overlap yet.
"""

result = run_fusion(
    headlines,
    politician_summary,
    validated
)

print("\nFINAL INTELLIGENCE\n")
print(result)

print("\nRouting alerts...\n")

route_alert(result)
