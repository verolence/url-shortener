import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path("shortener.db")

def get_connection(db_path: Path = DEFAULT_DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.isolation_level = None  # для автоматического commit/close
    return conn


def init_db(db_path: Path = DEFAULT_DB_PATH):
    with get_connection(db_path) as conn:
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