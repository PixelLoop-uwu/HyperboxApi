import sys

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger

from .routes import auth, resources, skins, modpacks
from .config import config


api = FastAPI()

@api.get("/")
def main():
  return RedirectResponse(config.REDIRECT_URL)

api.include_router(auth.router)
api.include_router(resources.router)
api.include_router(skins.router)
api.include_router(modpacks.router)


logger.remove()

logger.add(
  sys.stderr,
  level="DEBUG",
  format=
  "<green>{time:HH:mm:ss}</green> | "
    "<level>{level}</level> | "
    "<cyan>{name}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)
