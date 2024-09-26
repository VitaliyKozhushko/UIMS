from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    logger.info('Application startup complete.')
    yield
    logger.info('Application shutdown initiated.')

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
