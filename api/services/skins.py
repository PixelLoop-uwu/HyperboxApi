import base64
from PIL import Image
from io import BytesIO
from loguru import logger

from api.config import config


def upload_skin(UploadSkinForm) -> dict:
  user_path = config.DATA_FOLDER / "players" / UploadSkinForm.username
  user_path.mkdir(parents=True, exist_ok=True)

  if UploadSkinForm.app_token != config.APP_TOKEN:
    return {"status": "error", "error": "app_token_is_invalid"} 

  try:
    img_bytes = base64.b64decode(UploadSkinForm.base64data)
    img = Image.open(BytesIO(img_bytes)).convert("RGBA")

  except Exception as e:
    logger.error(str(e))
    return {"status": "error", "error": "64_data_is_invalid"} 


  # Save skin
  img.save(user_path / "skin.png", format="PNG")

  # Crop avatar
  x1, y1, w1, h1 = (8, 8, 8, 8)   # first layer
  x2, y2, w2, h2 = (40, 8, 8, 8)  # second layer

  layer1 = img.crop((x1, y1, x1 + w1, h1 + y1))
  layer2 = img.crop((x2, y2, x2 + w2, h2 + y2))
  
  avatar = Image.new("RGBA", layer1.size)
  avatar.paste(layer1, (0, 0), layer1)
  avatar.paste(layer2, (0, 0), layer2)

  avatar.save(user_path / "avatar.png", format="PNG")

  return {"status": True}