from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from base import Base 

DB_URL = "sqlite+aiosqlite:///./db.sqlite3"

engine: AsyncEngine = create_async_engine(
    DB_URL,
    echo=True,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_async_session():
    """
    Провайдер асинхронной сессии.
    """
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    """
    Создание всех таблиц в БД.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def reset_db(engine: AsyncEngine):
    """
    Очистка всех таблиц в БД (для тестов).
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
