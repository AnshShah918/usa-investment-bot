POLICY_KEYWORDS = [

    "trump",
    "white house",
    "pentagon",
    "defense",
    "tariff",
    "iran",
    "china",
    "congress",
    "senate",
    "executive",
    "sanction",
    "commerce",
    "treasury",
    "sec",
    "doj",
    "military",
    "drone",
    "trade war",
    "export control",
    "subsidy",
    "policy"
]

def filter_policy_news(news):

    filtered = []

    for item in news:

        title = (
            item["title"]
            .lower()
        )

        if any(
            k in title
            for k in POLICY_KEYWORDS
        ):

            filtered.append(item)

    return filtered
