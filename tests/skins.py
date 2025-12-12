import httpx
from dotenv import load_dotenv
import os
import base64

load_dotenv()

APP_TOKEN = os.getenv("app_token")
ADMIN_TOKEN = os.getenv("admin_token")


def image_to_base64(path):
    with open(path, "rb") as f:
        img_bytes = f.read()
    return base64.b64encode(img_bytes).decode("utf-8")


b64 = image_to_base64("tests/skin.png")

auth_data = {
    "username": "goida",
    "base64data": b64,
    "app_token": APP_TOKEN
}

response = httpx.post("http://127.0.0.1:5493/skins/upload_skin", json=auth_data)
print(response.text)



