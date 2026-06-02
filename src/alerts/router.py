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
