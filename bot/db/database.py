from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncConnection
from sqlalchemy.orm import DeclarativeBase

from bot.config.config import settings

async_engine = create_async_engine(
    url = settings.get_async_url,
    echo = False,
    pool_size = 10,
    max_overflow = 5
)

session_factory = async_sessionmaker(
    async_engine,
    autoflush= True
)

class Base(DeclarativeBase):
    pass