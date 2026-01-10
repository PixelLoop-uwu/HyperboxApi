from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import config

DB_URL = f"sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DB_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
  session = SessionLocal()
  try:
    yield session
  finally:
    await session.close()