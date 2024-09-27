import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import Base
from environs import Env
import os
from pathlib import Path

env = Env()
ENVIRONMENT = env('ENVIRONMENT', default='local')

BASE_DIR = Path(__file__).resolve().parent

if ENVIRONMENT == 'docker':
    env.read_env(os.path.join(BASE_DIR, '.env.backend.docker'))
else:
    env.read_env(os.path.join(BASE_DIR, '.env'))

env.read_env(".env")


DATABASE_URL = f'postgresql+asyncpg://{env("USER_DB")}:{env("PASSWD_DB")}@{env("HOST_DB")}:{env("PORT_DB")}/{env("NAME_DB")}'

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with async_session() as session:
        yield session


async def main():
    async for session in get_db():
        result = await session.execute(text('SELECT * FROM warehouse'))
        items = result.scalars().all()
        print('items:', items)


if __name__ == '__main__':
    asyncio.run(main())
