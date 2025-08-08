from sqlalchemy.ext.asyncio import create_async_engine
from models import Base
from settings import AppSettings

# Get settings
settings = AppSettings()

# Use the database URL from settings
SQLALCHEMY_DATABASE_URL = settings.constructed_database_url
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

async def init_db() -> None:
    async with engine.begin() as conn:
        # Create all tables in the database (only if they don't exist)
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized successfully.")

from typing import Annotated

from database import engine
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, autocommit=False, autoflush=False
)


async def get_db_session():
    try:
        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()


DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]