import httpx
from dotenv import load_dotenv
import os 

load_dotenv()

APP_TOKEN = os.getenv("app_token")
ADMIN_TOKEN = os.getenv("admin_token")
host = "http://127.0.0.1:5493/users"


auth_data = {"username": "zalupchik", "app_token": APP_TOKEN}
responce = httpx.post(f"{host}/register", json=auth_data)
print(responce.text)

auth_data = {"username": "zalupchik", "token": "unPG0J1-kFkqI-G28WQ-c5o", "app_token": APP_TOKEN}
responce = httpx.post(f"{host}/login", json=auth_data)
print(responce.text)

auth_data = {"username": "zalupchik", "admin_token": ADMIN_TOKEN}
responce = httpx.post(f"{host}/delete", json=auth_data)
print(responce.text)



