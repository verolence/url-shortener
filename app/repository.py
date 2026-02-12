from app.database import get_connection
from datetime import datetime

def insert_url(code: str, original_url: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO urls (code, original_url, created_at) VALUES (?, ?, ?)",
            (code, original_url, datetime.utcnow().isoformat())
        )
        conn.commit()

def get_url_by_code(code: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT original_url FROM urls WHERE code = ?", (code,))
        row = cursor.fetchone()
        return row[0] if row else None