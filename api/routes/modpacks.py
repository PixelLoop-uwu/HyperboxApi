from fastapi import APIRouter, HTTPException
from loguru import logger

from api.config import config 
from api.utils import read_json
from api.models import Modpack


router = APIRouter()

@router.get("/modpacks/getlist", response_model=list[Modpack])
async def get_modpacks() -> list:
  return read_json(config.DATA_FOLDER / "modpacks.json")

@router.get("/modpacks/{modpack}")
async def get_modpack_info(modpack) -> dict:
  try:
    return read_json(config.DATA_FOLDER / f"modpacks/{modpack}.json")
  except:
    raise HTTPException(status_code=404, detail="Модпак не найден") 
  

