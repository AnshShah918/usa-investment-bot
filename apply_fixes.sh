#!/bin/bash
set -e
echo "Applying all fixes..."

# ── FIX 1: Correct Gemini model name ──────────────────────────────────────────
cat > src/ai/gemini_client.py << 'EOF'
from datetime import date
from google import genai
import os

from src.config import GEMINI_API_KEY
from src.ai.gemini_usage import increment_request, reset_usage, get_usage
from src.ai.guardrails import can_use_gemini

client = genai.Client(
    api_key=GEMINI_API_KEY
)

PRIMARY_MODEL = "gemini-2.0-flash-lite"

USAGE_DATE_FILE = "gemini_usage_date.txt"

def _auto_reset_if_new_day():
    today = str(date.today())
    if os.path.exists(USAGE_DATE_FILE):
        with open(USAGE_DATE_FILE) as f:
            if f.read().strip() == today:
                return
    reset_usage()
    with open(USAGE_DATE_FILE, "w") as f:
        f.write(today)

def ask_gemini(prompt):

    _auto_reset_if_new_day()

    if not can_use_gemini():
        print("Gemini daily limit reached")
        return None

    try:
        response = client.models.generate_content(
            model=PRIMARY_MODEL,
            contents=prompt
        )

        parts = []

        if (
            hasattr(response, "candidates")
            and response.candidates
        ):
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    parts.append(part.text)

        text = "\n".join(parts).strip()

        if text:
            increment_request()

        return text

    except Exception as e:
        print("Gemini failed:", e)
        return None
EOF
echo "✓ Fix 1: gemini_client.py updated (model name + daily auto-reset)"

# ── FIX 2: Delete duplicate telegram_bot.py ───────────────────────────────────
rm -f src/alerts/telegram_bot.py
echo "✓ Fix 2: telegram_bot.py deleted"

# ── FIX 3: Fix congress.py endpoint ───────────────────────────────────────────
cat > src/collectors/congress.py << 'EOF'
import requests

URL = "https://senatestockwatcher.com/api/trades?pageSize=10&page=0"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_congress_trades():
    try:
        response = requests.get(URL, headers=headers, timeout=30)

        if response.status_code != 200:
            print("Fetch failed:", response.status_code)
            return []

        return response.json()

    except Exception as e:
        print("Error:", e)
        return []
EOF
echo "✓ Fix 3: congress.py endpoint fixed"

# ── FIX 4: gemini_usage.py — safe int parsing ─────────────────────────────────
cat > src/ai/gemini_usage.py << 'EOF'
import os

USAGE_FILE = "gemini_usage.txt"

def get_usage():
    if not os.path.exists(USAGE_FILE):
        return 0
    with open(USAGE_FILE, "r") as f:
        value = f.read().strip()
        if not value:
            return 0
        try:
            return int(value)
        except ValueError:
            return 0

def increment_request():
    current = get_usage()
    current += 1
    with open(USAGE_FILE, "w") as f:
        f.write(str(current))

def reset_usage():
    with open(USAGE_FILE, "w") as f:
        f.write("0")
EOF
echo "✓ Fix 4: gemini_usage.py safe int parsing added"

# ── FIX 5: Wire politician trades into run_scan.py ────────────────────────────
cat > src/scanner/run_scan.py << 'EOF'
from src.news.news_collector import get_news
from src.news.policy_filter import filter_policy_news
from src.news.stock_mapper import discover_stocks
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

    stocks = discover_stocks(policy_news)

    validated = []

    for s in stocks:
        quote = get_quote(s["ticker"])
        if quote:
            validated.append({
                "ticker": s["ticker"],
                "why": s["why"],
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

    result = run_fusion(headlines, politician_summary, validated)

    print("\nFINAL INTELLIGENCE\n")
    print(result)

    route_alert(result)

    return result
EOF
echo "✓ Fix 5: run_scan.py wired with real politician trades + init_db"

# ── FIX 6: Guard against None in router.py ────────────────────────────────────
cat > src/alerts/router.py << 'EOF'
import re
from src.alerts.telegram_alert import send_telegram

def route_alert(result):

    if not result:
        print("No result to route")
        return

    blocks = re.split(r'\n(?=\d+\.)', result)

    sent = 0

    for block in blocks:

        ticker = re.search(r"Ticker:\s*(.*)", block)
        conviction = re.search(r"Conviction:\s*(.*)", block, re.IGNORECASE)
        stage = re.search(r"Stage:\s*(.*)", block, re.IGNORECASE)
        followup = re.search(r"FollowUp:\s*(.*)", block, re.IGNORECASE)

        if not ticker:
            continue

        conviction_text = conviction.group(1).upper() if conviction else ""
        stage_text = stage.group(1).upper() if stage else ""
        followup_text = followup.group(1).upper() if followup else ""

        should_send = (
            "HIGH" in conviction_text
            or "EARLY" in stage_text
            or ("MOVING" in stage_text and len(followup_text) > 0)
        )

        if should_send:
            message = "🚨 MARKET OPPORTUNITY\n\n" + block.strip()
            print("Sending:", ticker.group(1))
            send_telegram(message)
            sent += 1

    print("Alerts sent:", sent)
EOF
echo "✓ Fix 6: router.py None guard added"

# ── FIX 7: Add missing __init__.py files ──────────────────────────────────────
touch src/ai/__init__.py
touch src/market/__init__.py
touch src/news/__init__.py
touch src/scanner/__init__.py
touch src/db/__init__.py
echo "✓ Fix 7: Missing __init__.py files created"

# ── FIX 8: Broaden news feeds in news_collector.py ────────────────────────────
cat > src/news/news_collector.py << 'EOF'
import feedparser

RSS_FEEDS = [
    "https://news.google.com/rss/search?q=Trump+stock+market",
    "https://news.google.com/rss/search?q=Trump+tariffs",
    "https://news.google.com/rss/search?q=Trump+economy",
    "https://news.google.com/rss/search?q=US+stock+market",
    "https://news.google.com/rss/search?q=US+stocks+earnings",
    "https://news.google.com/rss/search?q=Federal+Reserve+interest+rates",
]

def get_news():

    news = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            news.append({
                "title": entry.title,
                "link": entry.link,
                "published": getattr(entry, "published", "Unknown")
            })

    return news
EOF
echo "✓ Fix 8: news_collector.py broadened with 2 extra feeds"

echo ""
echo "✅ All fixes applied successfully!"
