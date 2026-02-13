from app.database import get_connection, DEFAULT_DB_PATH
from datetime import datetime, timezone
from pathlib import Path

def insert_url(code: str, original_url: str, db_path: Path = DEFAULT_DB_PATH):
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO urls (code, original_url, created_at) VALUES (?, ?, ?)",
            (code, original_url, datetime.now(timezone.utc).isoformat())
        )
        conn.commit()

def get_url_by_code(code: str, db_path: Path = DEFAULT_DB_PATH):
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT original_url FROM urls WHERE code = ?", (code,))
        row = cursor.fetchone()
        return row[0] if row else None