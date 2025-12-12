import json
import bcrypt
from pathlib import Path


def read_json(file_path: Path) -> dict:
  with file_path.open("r", encoding="utf-8") as f:
    return json.load(f)
  

def hash_password(password: str) -> str:
  """Generate random password hash"""
  return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
  """Compare password with hash"""
  return bcrypt.checkpw(password.encode(), hashed.encode())

