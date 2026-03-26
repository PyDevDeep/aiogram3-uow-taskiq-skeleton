from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.core.config import settings

# Engine configuration with connection pooling
engine = create_async_engine(
    url=settings.database_url,
    echo=settings.ENVIRONMENT == "development",
    pool_size=10,
    max_overflow=20,
)

async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False
)
