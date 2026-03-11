import sqlite3

DB_PATH = "database/database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS content_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        content_type TEXT,
        topic TEXT,
        audience TEXT,
        purpose TEXT,
        tone TEXT,
        length TEXT,
        keywords TEXT,
        instructions TEXT,
        tier TEXT,
        status TEXT DEFAULT 'new',
        created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        delivery_time TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
