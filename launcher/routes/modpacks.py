from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from config import config


router = APIRouter()

@router.get("/")
async def get_file_by_path():

  modpacks_json = config.DATA_FOLDER / "modpacks.json"

  return FileResponse(
    path=modpacks_json, 
    filename=modpacks_json.name,
    media_type='application/json'
  )

@router.get("/get")
async def get_file_by_path(modpack: str):

  modpacks_json = config.DATA_FOLDER / "modpacks" / f"{modpack}.json"

  if not str(modpacks_json).startswith(str(config.DATA_FOLDER)):
    raise HTTPException(status_code=403, detail="Съебался")

  return FileResponse(
    path=modpacks_json, 
    filename=modpacks_json.name,
    media_type='application/json'
  )