from pydantic import BaseModel
from typing import List


class LoginForm(BaseModel):
  username: str
  token: str
  app_token: str

class RegisterForm(BaseModel):
  username: str
  token: str
  app_token: str

class DeleteForm(BaseModel):
  username: str
  admin_token: str


class UploadSkinForm(BaseModel):
  username: str
  base64data: str
  app_token: str
  

class Modpack(BaseModel):
  id: int
  title: str
  version: str
  description: List[str]
  folder: str