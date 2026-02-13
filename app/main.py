from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from app.database import init_db
from app.logging_config import setup_logging
from pydantic import BaseModel
from app.service import generate_code, is_valid_url
from app.repository import insert_url, get_url_by_code
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    init_db()
    yield

logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)

BASE_URL = "http://localhost:8000"

class URLItem(BaseModel):
    url: str

@app.post("/shorten", status_code=201)
def shorten_url(item: URLItem):
    if not is_valid_url(item.url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    code = generate_code()
    insert_url(code, item.url)

    return {"short_url": f"{BASE_URL}/{code}"}

@app.get("/{code}")
def redirect_to_url(code: str):
    original_url = get_url_by_code(code)
    if original_url:
        logger.info(f"Redirecting code {code} to {original_url}")
        return RedirectResponse(url=original_url, status_code=307)
    else:
        logger.warning(f"Code {code} not found")
        raise HTTPException(status_code=404, detail="URL not found")