from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, create_async_engine
from models import async_session

DB_URL = "sqlite+aiosqlite:///./db.sqlite3"

Base = declarative_base()
engine: AsyncEngine = create_async_engine(DB_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False  # явно указываем autoflush, чтобы избежать значения по умолчанию
)  # type: ignore

async def get_async_session():
    """
    Провайдер асинхронной сессии.
    """
    async with async_session() as session:
        yield session


async def init_db():
    """
    Создание всех таблиц в БД.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def reset_db():
    """
    Очистка всех таблиц в БД. (для тестов в мое случае)
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
