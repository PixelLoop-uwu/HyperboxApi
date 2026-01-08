from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.models import User
from core.utils import verify_password
import json
from typing import Union


async def create_user(session: AsyncSession, minecraft_username: str, hash_password: str, discord_id: str = None) -> str:
  # Проверка существования
  result = await session.execute(select(User).filter_by(minecraft_username=minecraft_username))
  if result.scalar_one_or_none():
    raise ValueError("user_already_exists")

  new_user = User(
    minecraft_username=minecraft_username,
    password_hash=hash_password,
    discord_id=discord_id
  )
  session.add(new_user)
  await session.commit()
  return new_user.uid

async def get_user_by_identifier(session: AsyncSession, identifier: str) -> User | None:
  """Поиск пользователя по нику, Discord ID или uid. Возвращает объект User"""
  result = await session.execute(
    select(User).filter(
      or_(User.minecraft_username == identifier, User.discord_id == identifier, User.uid == identifier)
    )
  )
  return result.scalar_one_or_none()

async def update_assets_tokens(session: AsyncSession, user_or_uid: Union[User, str, int], token: str, action: str = "add") -> bool:
  """action: add, check, delete"""
  if not isinstance(user_or_uid, User):
    user = await get_user_by_identifier(session, user_or_uid)
  else:
    user = user_or_uid

  if not user:
    return False
    
  tokens = json.loads(user.assets_tokens or "[]")
  
  if action == "check":
    return token in tokens

  modified = False
  if action == "add" and token not in tokens:
    tokens.append(token)
    modified = True

  elif action == "delete":
    if token in tokens:
      tokens.remove(token)
      modified = True
    elif token == "all":
      tokens = []
      modified = True
    
  if modified:
    user.assets_tokens = json.dumps(tokens)
    session.add(user)
    await session.commit()
    
  return user.minecraft_username

async def get_user_info_dict(session: AsyncSession, identifier: str) -> dict | None:
  user = await get_user_by_identifier(session, identifier)
  if not user:
    raise ValueError("user_not_found")
  return {
    "discord_id": user.discord_id,
    "minecraft_username": user.minecraft_username,
    "uid": user.uid,
    "creation_date": user.creation_date.isoformat()
  }

async def delete_user(session: AsyncSession, identifier: str) -> bool:
  user = await get_user_by_identifier(session, identifier)
  if not user:
    raise ValueError("user_not_found")
  await session.delete(user)
  await session.commit()
  return user.minecraft_username

async def update_user_password(session: AsyncSession, identifier: str, new_password_hash: str) -> str:
  user = await get_user_by_identifier(session, identifier)
  
  if not user:
    raise ValueError("user_not_found")
  
  user.password_hash = new_password_hash
  
  session.add(user)
  await session.commit()
  return user.minecraft_username