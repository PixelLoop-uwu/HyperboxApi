from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from core.schemas import *
from auth.dependencies import admin_check
from core.services.users import create_user, authenticate, delete_user, get_user_info, recovery_token
from core.database.session import get_db


router = APIRouter()

@router.post("/register")
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db), admin = Depends(admin_check)):
  try:
    password_token = await create_user(db, data)
  except ValueError as e:
    return {"status": "error", "error": str(e)}
  
  logger.success(f"Добавлен пользователь {data.minecraft_username}.")
  return {"status": "ok", "password_token": password_token}


@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
  login_data = authenticate(db, data)
  logger.info(f"{data.minecraft_username} авторизовался.")
  return await login_data


@router.delete("/delete")
async def delete(identifier: str, db: AsyncSession = Depends(get_db), admin = Depends(admin_check)):
  try:
    username = await delete_user(db, identifier)
  except ValueError as e:
    return {"status": "error", "error": str(e)}
  
  logger.success(f"Учетная запись {username} удалена.")
  return {"status": "ok", "minecraft_username": username}


@router.get("/user_info")
async def user_info(identifier: str, type: str, db: AsyncSession = Depends(get_db)):
  try:
    data = await get_user_info(db, identifier, type)
  except ValueError as e:
    return {"status": "error", "error": str(e)}
  
  return {"status": "ok", "info": data}


@router.patch("/recovery")
async def recovery(data: RecoveryRequest, db: AsyncSession = Depends(get_db), admin = Depends(admin_check)):
  try:
    new_data = await recovery_token(db, data)

  except ValueError as e:
    return {"status": "error", "error": str(e)}
  
  logger.success(f"Токен для {new_data['username']} обновлен.")
  return {"status": "ok", "new_token": new_data['password_token']}

