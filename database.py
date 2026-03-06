import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blog_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            industry TEXT,
            keywords TEXT,
            blog_type TEXT,
            gumroad_receipt TEXT,
            payment_status TEXT,
            status TEXT,
            created_at TEXT,
            scheduled_delivery TEXT,
            folder_path TEXT
        )
    """)

    conn.commit()
    conn.close()

def get_today_count():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT COUNT(*) FROM blog_requests
        WHERE created_at LIKE ?
    """, (f"{today}%",))

    count = cursor.fetchone()[0]
    conn.close()
    return count
