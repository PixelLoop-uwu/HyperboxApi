import httpx
import json

BASE_URL = "http://127.0.0.1:8000/users"
# Токен, который ожидает твой admin_check
ADMIN_HEADERS = {"Authorization": "Bearer 9hB0NXQdeA{}GqQlow|DKGjHYMaGc1FaW#k0VMQZ%S9b*t*YWTmf"}

def run_benchmarks():
  with httpx.Client(base_url=BASE_URL, trust_env=False) as client:
    
    # 1. ТЕСТ REGISTER
    print("\n--- Testing Register ---")
    reg_data = {
      "discord_id": "123456789",
      "minecraft_username": "SteveCase"
    }
    r = client.post("/register", json=reg_data, headers=ADMIN_HEADERS)
    print(f"Register Status: {r.status_code}")
    print(f"Response: {r.json()}")
    
    password_token = r.json().get("password_token") if r.status_code == 200 else None

    # 2. ТЕСТ LOGIN (если регистрация успешна)
    if password_token:
      print("\n--- Testing Login ---")
      login_data = {
        "minecraft_username": "SteveCase",
        "token": password_token
      }
      r = client.post("/login", json=login_data)
      print(f"Login Status: {r.status_code}")
      print(f"Response: {r.json()}")

    # 3. ТЕСТ USER_INFO
    print("\n--- Testing User Info ---")
    info_data = {
      "identifier": "SteveCase",
      "type": "minecraft" # или "discord" в зависимости от твоей логики
    }
    r = client.get("/user_info", params=info_data) # GET запрос с параметрами
    # Если твой роут ждет тело в GET (UserInfoRequest), используй json=info_data
    # Но по стандарту лучше использовать params или передать через POST
    print(f"Info Status: {r.status_code}")
    print(f"Response: {r.json()}")

    # 4. ТЕСТ RECOVERY
    print("\n--- Testing Recovery ---")
    rec_data = {"discord_id": "123456789"}
    r = client.patch("/recovery", json=rec_data, headers=ADMIN_HEADERS)
    print(f"Recovery Status: {r.status_code}")
    print(f"Response: {r.json()}")

    # 5. ТЕСТ DELETE
    print("\n--- Testing Delete ---")
    del_data = {"discord_id": "123456789"}
    r = client.request("DELETE", "/delete", json=del_data, headers=ADMIN_HEADERS)
    # В httpx для DELETE с телом лучше использовать общую функцию request
    print(f"Delete Status: {r.status_code}")
    print(f"Response: {r.json()}")

if __name__ == "__main__":
  run_benchmarks()