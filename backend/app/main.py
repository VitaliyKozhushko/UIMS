import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db
from app.routers import appointments
from app.routers import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
  await create_db()
  logger.info('Application startup complete.')
  yield
  logger.info('Application shutdown initiated.')


app = FastAPI(lifespan=lifespan)

origins = [
  "http://localhost:3000",
  "http://127.0.0.1:3000"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

app.include_router(appointments.router)
app.include_router(config.router)
