from fastapi import APIRouter

from api.models import LoginForm, RegisterForm, DeleteForm
from api.services import login, register, delete

router = APIRouter()


@router.post("/users/login")
async def check_user(data: LoginForm) -> dict:
  return await login(data)

@router.post("/users/register")
async def create_user(data: RegisterForm) -> dict:
  return await register(data)

@router.post("/users/delete")
async def delete_user(data: DeleteForm) -> dict:
  return await delete(data)


# Удалить пользователя
# Удалить assets токен
