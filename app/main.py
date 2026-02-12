from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.database import init_db
from app.logging_config import setup_logging
from pydantic import BaseModel
from app.service import generate_code, is_valid_url
from app.repository import insert_url

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    init_db()
    yield

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