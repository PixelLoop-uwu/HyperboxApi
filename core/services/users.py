from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import generate_password_token, hash_password, create_asset_token, verify_password
from core.schemas import *
from core.database import users as database
from auth.jwt import create_jwt


async def create_user(db: AsyncSession, data: RegisterRequest) -> dict:
  password_token = generate_password_token()

  await database.create_user(
    session=db, 
    minecraft_username=data.minecraft_username, 
    hash_password=hash_password(password_token), 
    discord_id=data.discord_id
  )

  return password_token
  

async def authenticate(db: AsyncSession, data: LoginRequest) -> dict:
  user = await database.get_user_by_identifier(db, data.minecraft_username)
  
  if not user or not verify_password(data.token, user.password_hash):
    raise HTTPException(status_code=403, detail="Incorrect username or token")

  jwt = create_jwt(user.minecraft_username)
  new_asset_token = create_asset_token()

  await database.update_assets_tokens(db, user, new_asset_token, "add")

  return {
    "status": "ok",
    "jwt": jwt,
    "asset_token": new_asset_token,
    "uid": user.uid
  }


async def delete_user(db: AsyncSession, identifier: str) -> dict:
  # Удаление папки игрока
  return await database.delete_user(db, identifier)


async def get_user_info(db: AsyncSession, identifier: str, type: str) -> dict:
  return await database.get_user_info_dict(db, identifier)


async def recovery_token(db: AsyncSession, data: RecoveryRequest) -> dict:
  password_token = generate_password_token()

  await database.update_user_password(
    db, 
    data.discord_id, 
    hash_password(password_token)
  )

  username = await database.update_assets_tokens(db, data.discord_id, "all", "delete")

  return {"password_token": password_token, "username": username}