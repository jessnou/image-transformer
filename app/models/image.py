from bson import Binary
from pymongo import MongoClient

class Image:
    def __init__(self, db):
        """
        Инициализация класса Image.
        :param db: Экземпляр базы данных MongoDB.
        """
        self.collection = db['images']  # Коллекция для хранения изображений

    def save_image(self, image_data, filename, format, size, url=None):
        """
        Сохраняет изображение в коллекцию MongoDB.
        :param image_data: Бинарные данные изображения.
        :param filename: Имя файла.
        :param format: Формат изображения (например, 'png', 'jpg').
        :param size: Словарь с размерами изображения (например, {'width': 800, 'height': 600}).
        :param url: URL изображения (опционально).
        """
        # Создаем документ для сохранения
        image_document = {
            'filename': filename,
            'image_data': Binary(image_data),  # Преобразуем данные в бинарный формат
            'format': format,
            'size': size,
            'url': url
        }

        # Вставляем документ в коллекцию
        result = self.collection.insert_one(image_document)
        return result.inserted_id  # Возвращаем ID сохраненного документа