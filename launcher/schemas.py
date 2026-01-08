from pydantic import BaseModel

class UploadSkinForm(BaseModel):
  minecraft_username: str
  base64data: str


