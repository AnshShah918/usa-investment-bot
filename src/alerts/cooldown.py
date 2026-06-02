from datetime import datetime

LAST_DEEP = None
COOLDOWN = 30

def can_run_deep():

    global LAST_DEEP

    now = datetime.now()

    if LAST_DEEP:

        delta = (
            now - LAST_DEEP
        ).seconds

        if delta < COOLDOWN:
            return False

    LAST_DEEP = now

    return True
