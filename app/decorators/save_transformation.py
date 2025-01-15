from functools import wraps
from io import BytesIO
import uuid
from PIL import Image
from fastapi import HTTPException
from typing import Callable
import logging
from app.models.image import Image as ImageModel

from app.dependencies.database import get_mongo_db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Декоратор для сохранения преобразованного изображения в MongoDB
def save_to_mongo(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Выполняем основную функцию (например, стилизацию изображения)
            result_image = func(*args, **kwargs)

            # Проверяем, что результат является изображением
            if isinstance(result_image, Image.Image):
                # Преобразуем изображение в байты
                image_bytes = BytesIO()
                result_image.save(image_bytes, format="PNG")
                image_data = image_bytes.getvalue()

                # Получаем имя файла и другие данные
                filename = kwargs.get("filename", f"{uuid.uuid4().hex}.png")
                format = "png"
                size = {"width": result_image.width, "height": result_image.height}

                # Сохраняем изображение в MongoDB
                db = get_mongo_db()  # Получаем подключение к MongoDB
                image_handler = ImageModel(db)
                image_handler.save_image(image_data, filename, format, size, url=None)

            return result_image
        except Exception as e:
            # Логирование ошибок
            logger.error("Error saving the image to MongoDB: %s", e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

    return wrapper