from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class config:
  DATA_FOLDER = Path("launcher/DATA")
  REDIRECT_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ/"

  MINI_APP_SECRET = os.getenv("MINI_APP_SECRET")

  JWT_SECRET = os.getenv("JWT_SECRET")
  JWT_ALGORITHM = "HS256"

  SERVER_RCON = {
    "host": "123123",
    "port": 1231,
    "password": "Goidaa"
  }