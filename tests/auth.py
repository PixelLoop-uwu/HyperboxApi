import httpx
from dotenv import load_dotenv
import os 

load_dotenv()

APP_TOKEN = os.getenv("app_token")
ADMIN_TOKEN = os.getenv("admin_token")


auth_data = {"username": "goida", "token": "123123123123", "app_token": APP_TOKEN}
responce = httpx.post("http://127.0.0.1:5493/users/register", json=auth_data)
print(responce.text)

auth_data = {"username": "goida", "token": "123123123123", "app_token": APP_TOKEN}
responce = httpx.post("http://127.0.0.1:5493/users/login", json=auth_data)
print(responce.text)

auth_data = {"username": "goida", "token": "123123123123", "admin_token": ADMIN_TOKEN}
responce = httpx.post("http://127.0.0.1:5493/users/delete", json=auth_data)
print(responce.text)



