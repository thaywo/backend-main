import os
from dotenv import load_dotenv
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

connection_string = URL.create(
    "postgresql+asyncpg",
    username="postgres",
    password="@T25r5s540",
    host="localhost",
    port=5433,
    database="assignment",
)

async_engine = create_async_engine(
    connection_string,
    echo=True,
    pool_size=6,
    max_overflow=2,
    pool_recycle=1800,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

async def async_get_db():
    async with AsyncSessionLocal() as session:
        yield session
