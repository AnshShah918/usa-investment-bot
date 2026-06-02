import feedparser

RSS_FEEDS = [
    "https://news.google.com/rss/search?q=Trump+stock+market",
    "https://news.google.com/rss/search?q=Trump+tariffs",
    "https://news.google.com/rss/search?q=Trump+economy",
    "https://news.google.com/rss/search?q=US+stock+market"
]

def get_news():

    news = []

    for url in RSS_FEEDS:

        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:

            news.append({
                "title": entry.title,
                "link": entry.link,
                "published": getattr(
                    entry,
                    "published",
                    "Unknown"
                )
            })

    return news
