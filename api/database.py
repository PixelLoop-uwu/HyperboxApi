from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import json
from pathlib import Path

from api.bases import Base, User
from api.utils import verify_password, hash_password
from api.config import config


class DatabaseManager:
  def __init__(self, db_url = f"sqlite+aiosqlite:///./data.db"):
    self.engine = create_async_engine(db_url, echo=True)
    self.Session = sessionmaker(
      bind=self.engine,
      expire_on_commit=False,
      class_=AsyncSession
    )

  async def _table_check(self):
    async with self.engine.begin() as conn:
      await conn.run_sync(Base.metadata.create_all)

  async def __aenter__(self):
    await self._table_check()
    return self

  async def __aexit__(self, exc_type, exc, tb):
    await self.engine.dispose()


  async def check_user(self, username: str, password: str) -> bool:
    """Compare username with password"""
    async with self.Session() as session:  
      result = await session.execute(select(User).filter_by(username=username))
      user = result.scalar_one_or_none()
      if not user:
        return False
      return verify_password(password, user.password_hash)
    
  async def create_user(self, username: str, password: str) -> bool:
    """Create a new user. Returns true if the user is created, false if the user exists."""
    async with self.Session() as session:
      result = await session.execute(select(User).filter_by(username=username))
      existing_user = result.scalar_one_or_none()
      if existing_user:
        return False

      new_user = User(
        username=username,
        password_hash=hash_password(password),
        assets_tokens=json.dumps([])
      )
      session.add(new_user)
      await session.commit()
      return True
    
  async def delete_user(self, username: str) -> bool:
    """Delete user by username. Return true if the user is deleted, false if the user is not found."""
    async with self.Session() as session:
      result = await session.execute(select(User).filter_by(username=username))
      user = result.scalar_one_or_none()
      if not user:
        return False 

      await session.delete(user)
      await session.commit()
      return True


  async def create_assets_token(self, username: str, token: str) -> bool:
    """"""
    async with self.Session() as session:
      result = await session.execute(select(User).filter_by(username=username))
      user = result.scalar_one_or_none()
      if not user:
        return False
      tokens = json.loads(user.assets_tokens or "[]")
      if token not in tokens:
        tokens.append(token)
        user.assets_tokens = json.dumps(tokens)
        session.add(user)
        await session.commit()
      return True

  async def check_assets_token(self, username: str, token: str, delete: bool) -> bool:
    """"""
    async with self.Session() as session:
      result = await session.execute(select(User).filter_by(username=username))
      user = result.scalar_one_or_none()
      if not user:
        return False
      tokens = json.loads(user.assets_tokens or "[]")
      if token not in tokens:
        return False
      if delete:
        tokens.remove(token)
        user.assets_tokens = json.dumps(tokens)
        session.add(user)
        await session.commit()
      return True