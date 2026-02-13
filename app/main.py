from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from pathlib import Path
import logging

from app.database import init_db, DEFAULT_DB_PATH
from app.logging_config import setup_logging
from app.service import generate_code, is_valid_url
from app.repository import insert_url, get_url_by_code


def get_db_path() -> Path:
    return DEFAULT_DB_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    init_db()
    yield

logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"

app = FastAPI(lifespan=lifespan)

class URLItem(BaseModel):
    url: str

@app.post("/shorten", status_code=201)
def shorten_url(item: URLItem, db_path: Path = Depends(get_db_path)):
    if not is_valid_url(item.url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    code = generate_code()
    insert_url(code, item.url, db_path=db_path)

    return {"short_url": f"{BASE_URL}/{code}"}

@app.get("/{code}")
def redirect_to_url(code: str, db_path: Path = Depends(get_db_path)):
    original_url = get_url_by_code(code, db_path=db_path)
    if original_url:
        logger.info(f"Redirecting code {code} to {original_url}")
        return RedirectResponse(url=original_url, status_code=307)
    else:
        logger.warning(f"Code {code} not found")
        raise HTTPException(status_code=404, detail="URL not found")