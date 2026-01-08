from pydantic import BaseModel


class RegisterRequest(BaseModel):
  minecraft_username: str
  discord_id: int

class LoginRequest(BaseModel):
  minecraft_username: str
  token: str

class RecoveryRequest(BaseModel):
  discord_id: int

class DeleteRequest(BaseModel):
  discord_id: int

class BanRequest(BaseModel):
  identifier: str
  type: str

class UserInfoRequest(BaseModel):
  identifier: str
  type: str
  