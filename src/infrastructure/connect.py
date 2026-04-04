from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.config import settings


async_engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
