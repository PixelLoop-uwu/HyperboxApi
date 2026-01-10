from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from loguru import logger

from config import config
from launcher.schemas import UploadSkinForm
from launcher.services import skins

from auth.dependencies import get_user, admin_check
from core.database.session import get_db


router = APIRouter()

@router.get("/get_avatar/{username}")
async def get_avatar_(username: str) -> None:
  path = config.DATA_FOLDER / "player_data" / username / "avatar.png"

  if not path.exists() or not path.is_file():
    return FileResponse(
      path=config.DATA_FOLDER / "player_data" / "avatar.png",
      filename=path.name,
      media_type="application/png"
    )

  return FileResponse(
    path=path,
    filename=path.name,
    media_type="application/png"
  )

@router.get("/get_skin/{username}")
async def get_skin_(username: str) -> None:
  path = config.DATA_FOLDER / "players" / username / "skin.png"

  if not path.exists() or not path.is_file():
    return FileResponse(
      path=config.DATA_FOLDER / "players" / "skin.png",
      filename=path.name,
      media_type="application/png"
    )

  return FileResponse(
    path=path,
    filename=path.name,
    media_type="application/png"
  )

@router.post("/upload_skin")
async def upload_skin_(data: UploadSkinForm, user = Depends(get_user)) -> dict:
  if user["username"] != data.minecraft_username:
    raise HTTPException(403, f"Only for {user['username']}")
  
  try:
    logger.info(f"Скин {data.minecraft_username} обновлен")
    return skins.upload_skin(data)
  
  except ValueError as e:
    return {"status": "error", "error": str(e)}
  

@router.delete("/delete_skin")
async def delete_skin(identifier: str, db = Depends(get_db), admin = Depends(admin_check)):
  try:
    username = await skins.delete_skin(db, identifier)
    logger.info(f"Скин {username} удален")
    return {"status": 'ok'}
  except ValueError as e:
    return {"status": "error", "error": str(e)}
