from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from loguru import logger

from api.config import config 


router = APIRouter()

@router.get("/resources/{file_path:path}")
async def get_libraries(file_path: str) -> None:
  path = config.DATA_FOLDER / file_path

  if not path.exists() or not path.is_file():
    raise HTTPException(status_code=404, detail="Файл не найден")

  if path.suffix.lower() == ".json":
    return FileResponse(
      path=path,
      filename=path.name,
      media_type="application/json"
    )

  return FileResponse(
    path=path,
    filename=path.name,
    media_type="application/octet-stream"
  )


