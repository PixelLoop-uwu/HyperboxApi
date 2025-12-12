from fastapi import APIRouter
from fastapi.responses import FileResponse

from api.config import config
from api.models import UploadSkinForm


router = APIRouter()

@router.get("/skins/get_avatar/{username}")
async def get_avatar(username: str) -> None:
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

@router.get("/skins/get_skin/{username}")
async def get_skin(username: str) -> None:
  path = config.DATA_FOLDER / "player_data" / username / "skin.png"

  if not path.exists() or not path.is_file():
    return FileResponse(
      path=config.DATA_FOLDER / "player_data" / "skin.png",
      filename=path.name,
      media_type="application/png"
    )

  return FileResponse(
    path=path,
    filename=path.name,
    media_type="application/png"
  )

@router.post("/skins/upload_skin")
async def upload_skin(UploadSkinForm: UploadSkinForm) -> dict:
  return upload_skin(UploadSkinForm)