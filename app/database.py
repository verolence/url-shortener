import sqlite3
from pathlib import Path

DB_PATH = Path("shortener.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()