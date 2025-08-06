from sqlalchemy.ext.asyncio import create_async_engine
from models import Base

# Corrected database URL
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://fastapi:1121996sS@localhost/backend"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

async def init_db() -> None:
    async with engine.begin() as conn:
        # Create all tables in the database
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized successfully.")