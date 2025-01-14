import logging
from functools import wraps
import mongoengine as me
from io import BytesIO
from PIL import Image
from fastapi import HTTPException
from typing import Callable

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Декоратор для сохранения изображений в MongoDB
def save_to_mongo(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # Выполняем основную функцию (например, обработку изображения)
            response = await func(*args, **kwargs)
            
            # Логирование переменной response
            logger.info("Response received: %s", hasattr(response, 'body'))

            # Извлекаем изображение из ответа
            if hasattr(response, 'body') and isinstance(response.body, bytes):
                image_bytes = BytesIO(response.body)
                image = Image.open(image_bytes)

                # Получаем данные изображения
                image_data = image_bytes.getvalue()
                filename = kwargs.get("file").filename
                format = image.format.lower()
                size = {"width": image.width, "height": image.height}

                # Сохранение в MongoDB
                image_doc = Image()
                image_doc.save_image(image_data, filename, format, size, url=None)  # URL можно добавить позже, если нужно

            return response
        except Exception as e:
            # Логирование ошибок
            logger.error("Error processing the image: %s", e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return wrapper
