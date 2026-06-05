THEME_TO_STOCKS = {
    "DEFENSE": ["LMT", "RTX", "NOC", "GD"],
    "DRONES": ["AVAV", "KTOS"],
    "ENERGY": ["XOM", "CVX", "COP"],
    "SEMICONDUCTORS": ["NVDA", "AMD", "AVGO"],
    "AI_INFRASTRUCTURE": ["NVDA", "DELL", "SMCI"],
    "TARIFFS": ["CAT", "NUE", "TM"],
    "SHIPBUILDING": ["GD", "HII"],
}

KEYWORD_MAP = {
    "pentagon": ["DEFENSE"],
    "military": ["DEFENSE"],
    "defense": ["DEFENSE"],
    "drone": ["DRONES"],
    "iran": ["ENERGY"],
    "oil": ["ENERGY"],
    "chip": ["SEMICONDUCTORS"],
    "semiconductor": ["SEMICONDUCTORS"],
    "ai": ["AI_INFRASTRUCTURE"],
    "tariff": ["TARIFFS"],
    "trade": ["TARIFFS"],
    "navy": ["SHIPBUILDING"],
    "shipbuilding": ["SHIPBUILDING"]
}


def discover_stocks(news_items):

    scores = {}

    for item in news_items:

        title = item["title"].lower()

        for keyword, themes in KEYWORD_MAP.items():

            if keyword in title:

                for theme in themes:

                    for ticker in THEME_TO_STOCKS.get(theme, []):

                        scores[ticker] = scores.get(ticker, 0) + 1

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [ticker for ticker, _ in ranked[:10]]
