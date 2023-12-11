from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from functools import wraps
from config import CONFIG

SYNC_ENGINE = create_engine(f"postgresql://{CONFIG.DATABASE}")
ASYNC_ENGINE = create_async_engine(f"postgresql+asyncpg://{CONFIG.DATABASE}")
Session = sessionmaker(bind=SYNC_ENGINE)
Session1 = sessionmaker(bind=ASYNC_ENGINE, class_=AsyncSession)


def create_sync_session(func):
    def wrapper(**kwargs):
        with Session() as session:
            return func(**kwargs, session=session)
    return wrapper


def create_async_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with AsyncSession(bind=ASYNC_ENGINE) as session:
            return await func(*args, **kwargs, session=session)
    return wrapper
