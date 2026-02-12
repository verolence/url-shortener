from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.logging_config import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    init_db()
    yield

app = FastAPI(lifespan=lifespan)