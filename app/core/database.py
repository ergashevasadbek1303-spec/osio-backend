"""
Osio Restaurant — Database Connection (Neon PostgreSQL)
Async SQLAlchemy engine + session factory.
"""

# pyrefly: ignore [missing-import]
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


# Create database URL and ensure it has correct dialect for asyncpg
db_url = settings.DATABASE_URL
if not db_url.startswith("sqlite"):
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Create async engine based on database type
if db_url.startswith("sqlite"):
    engine = create_async_engine(
        db_url,
        echo=not settings.is_production,
    )
else:
    # Neon PostgreSQL/Render PostgreSQL uchun async engine
    # pool_pre_ping=True — serverless Neon/Render uchun muhim (idle connection'larni tekshiradi)
    engine = create_async_engine(
        db_url,
        echo=not settings.is_production,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Barcha modellar uchun base class."""
    pass


async def get_db():
    """
    Database session dependency.
    Har bir request uchun yangi session ochiladi va so'ngida yopiladi.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables():
    """Barcha jadvallarni yaratadi (development uchun)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
