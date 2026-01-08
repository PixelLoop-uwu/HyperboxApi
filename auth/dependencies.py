from fastapi import Header, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from config import config
from auth.jwt import decode_jwt


def admin_check(authorization: str = Header(...)):
  try:
    token = authorization.split(" ")[1] 
  except IndexError:
    raise HTTPException(401, "Invalid authorization header")

  if token != config.MINI_APP_SECRET:
    raise HTTPException(403, "Admin access required")
  return token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
def get_user(token: str = Depends(oauth2_scheme)):
  payload = decode_jwt(token)
  if not payload:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
  return payload

