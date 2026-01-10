from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from config import config


router = APIRouter()

@router.get("/get")
async def get_modpack(modpack: str):

  modpacks_json = config.DATA_FOLDER / "modpacks" / f"{modpack}.json"

  if not str(modpacks_json).startswith(str(config.DATA_FOLDER)):
    raise HTTPException(status_code=403, detail="Съебался")

  return FileResponse(
    path=modpacks_json, 
    filename=modpacks_json.name,
    media_type='application/json'
  )