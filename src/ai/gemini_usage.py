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
