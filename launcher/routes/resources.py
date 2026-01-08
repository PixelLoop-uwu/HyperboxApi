from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from config import config

router = APIRouter()

@router.get("/{file_path:path}")
async def get_file_by_path(file_path: str):
    
  safe_path = (config.DATA_FOLDER / file_path).resolve()

  if not str(safe_path).startswith(str(config.DATA_FOLDER)):
    raise HTTPException(status_code=403, detail="Съебался")

  if not safe_path.exists() or not safe_path.is_file():
    raise HTTPException(status_code=404, detail="Файл не найден")

  return FileResponse(
    path=safe_path, 
    filename=safe_path.name,
    media_type='application/octet-stream'
  )