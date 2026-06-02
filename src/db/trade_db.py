import sqlite3

DB_PATH = "src/db/signals.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS politician_trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trade_id TEXT UNIQUE,
        politician TEXT,
        ticker TEXT,
        transaction_type TEXT,
        trade_date TEXT,
        filed_date TEXT,
        asset_name TEXT,
        sector TEXT,
        estimated_value REAL
    )
    """)

    conn.commit()
    conn.close()


def save_trade(trade):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute("""
        INSERT OR IGNORE INTO politician_trades (
            trade_id,
            politician,
            ticker,
            transaction_type,
            trade_date,
            filed_date,
            asset_name,
            sector,
            estimated_value
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            trade["trade_id"],
            trade["politician"],
            trade["ticker"],
            trade["transaction_type"],
            trade["trade_date"],
            trade["filed_date"],
            trade["asset_name"],
            trade["sector"],
            trade["estimated_value"]
        ))

        conn.commit()

        return cur.rowcount == 1

    finally:
        conn.close()
