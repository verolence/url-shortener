import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sqlite3
from app.main import app, get_db_path
from app.database import init_db
from app.repository import insert_url, get_url_by_code
from app.service import generate_code

TEST_DB = Path("test.db")


def clear_tables(db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM urls")
        conn.commit()


@pytest.fixture(scope="module")
def client():
    if not TEST_DB.exists():
        init_db(db_path=TEST_DB)
    else:
        clear_tables(TEST_DB)
    
    app.dependency_overrides[get_db_path] = lambda: TEST_DB

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def test_create_shorten_url(client):
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 201
    data = response.json()
    assert "short_url" in data
    assert data["short_url"].startswith("http://localhost:8000/")
    code = data["short_url"].split("/")[-1]
    original = get_url_by_code(code, db_path=TEST_DB)
    assert original == "https://example.com"

def test_invalid_url(client):
    response = client.post("/shorten", json={"url": "invalid-url"})
    assert response.status_code == 400
    assert "Invalid URL" in response.json()["detail"]

def test_redirect(client):
    code = generate_code()
    insert_url(code, "https://example.com", db_path=TEST_DB)
    response = client.get(f"/{code}", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com"

def test_404_redirect(client):
    response = client.get("/nonexistentcode", follow_redirects=False)
    assert response.status_code == 404
    assert response.json()["detail"] == "URL not found"