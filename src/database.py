import os
import sys
from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(config_path)

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


DATABASE_URL = f"postgresql+asyncpg://postgres_test:kB0mQbPBpG5J87eISmSjWtXFbO3vT5mW@dpg-cnur28en7f5s73fc1lr0-a:5432/postgres_test_vwqu"


Base = declarative_base()


engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
