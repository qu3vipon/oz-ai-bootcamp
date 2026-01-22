from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DB_URL = "sqlite+aiosqlite:///./db.sqlite"

engine = create_async_engine(DB_URL)

AsyncSessionFactory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False, 
    autoflush=False, 
    expire_on_commit=False,
)
