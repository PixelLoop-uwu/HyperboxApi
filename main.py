from fastapi import FastAPI
from loguru import logger
import sys

from core.routes import router as core_router
from core.database.session import engine
from core.database.models import Base

from launcher.routes.modpacks import router as modpacks_router
from launcher.routes.resources import router as resources_router
from launcher.routes.skins import router as skins_router

def setup_logging():
  logger.remove()

  logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
  )

  logger.add(
    "logs/api_debug.log",
    rotation="10 MB", 
    retention="7 days",   
    compression="zip",   
    level="DEBUG",      
    encoding="utf-8"
  )


api = FastAPI(
  title="Hyperbox Api",
  version="0.1.0"
)


api.include_router(core_router, prefix="/users")
api.include_router(modpacks_router, prefix="/modpacks")
api.include_router(resources_router, prefix="/resources")
api.include_router(skins_router, prefix="/skins")


@api.on_event("startup")
async def startup():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
  
  setup_logging()


@api.get("/")
def main():
  return {"status": "ok"}
