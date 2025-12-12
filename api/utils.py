import json
import bcrypt
import random
import string
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


def generate_token() -> str:
  letters = string.ascii_letters
  digits = string.digits
  letters_digits = letters + digits

  def rnd_chars(length, chars):
    return ''.join(random.choice(chars) for _ in range(length))

  number = random.choice(range(0, 100, 4))
  number_str = f"{number:02d}" 

  token = (
    f"{rnd_chars(7, letters_digits)}-"  
    f"{rnd_chars(5, letters_digits)}-" 
    f"{random.choice(letters)}{number_str}{rnd_chars(2, letters_digits)}-"  
    f"{rnd_chars(3, letters_digits)}"  
  )

  return token
