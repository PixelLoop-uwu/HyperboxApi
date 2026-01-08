import bcrypt
import random
import string
import secrets


def hash_password(password: str) -> str:
  """Generate random password hash"""
  return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
  """Compare password with hash"""
  return bcrypt.checkpw(password.encode(), hashed.encode())


def generate_password_token() -> str:
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

def create_asset_token(length: int = 32) -> str:
  return secrets.token_urlsafe(length)
