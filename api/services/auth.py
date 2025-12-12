import secrets

from api.models import LoginForm, RegisterForm, DeleteForm
from api.database import DatabaseManager
from api.config import config
from loguru import logger

DBManager = DatabaseManager()

async def login(LoginForm: LoginForm) -> dict:
  if LoginForm.app_token != config.APP_TOKEN:
    logger.info(config.APP_TOKEN)
    logger.info(config.ADMIN_TOKEN)
    return {"status": "error", "error": "app_token_is_invalid"}

  async with DBManager as manager:
    if not await manager.check_user(LoginForm.username, LoginForm.token):
      return {"status": "error", "error": "token_or_username_is_incorrect"}
    
    assets_token = secrets.token_urlsafe(32)
    await manager.create_assets_token(LoginForm.username, assets_token)

    return {"status": True, "assets_token": assets_token}
  
async def register(RegisterForm: RegisterForm) -> dict:
  if RegisterForm.app_token != config.APP_TOKEN:
    return {"status": "error", "error": "app_token_is_invalid"}
  
  async with DBManager as manager:
    if await manager.create_user(RegisterForm.username, RegisterForm.token):
      return {"status": True}
    else:
      return {"status": "error", "error": "user_already_exists"}

async def delete(DeleteForm: DeleteForm) -> dict:
  if DeleteForm.admin_token != config.ADMIN_TOKEN:
    return {"status": "error", "error": "admin_token_is_invalid"}
  
  async with DBManager as manager:
    if await manager.delete_user(DeleteForm.username):
      return {"status": True}
    else:
      return {"status": "error", "error": "user_not_found"}
