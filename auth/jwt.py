from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from config import config


def create_jwt(username: str, hours: int = 2):
  now = datetime.now(timezone.utc)
  exp = now + timedelta(hours=hours)
  payload = {
    "username": username,
    "role": "user",
    "iat": int(now.timestamp()),
    "exp": int(exp.timestamp())
  }
  return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)

def decode_jwt(token: str):
  try:
    payload = jwt.decode(token, config.JWT_SECRET, algorithms=config.JWT_ALGORITHM)
    return payload
  except JWTError:
    return None
