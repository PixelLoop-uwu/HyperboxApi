from pathlib import Path
from dotenv import load_dotenv
import os 

load_dotenv()

class config:
  DATA_FOLDER = Path("DATA").resolve()
  REDIRECT_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ/"

  APP_TOKEN = os.getenv("app_token")
  ADMIN_TOKEN = os.getenv("admin_token")