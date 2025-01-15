from pymongo import MongoClient
from pymongo.uri_parser import parse_uri
from app.db_connection.connection import Connection
from app import config

class MongoConnection(Connection):
    def __init__(self):
        self.client = None
        self.db = None
        self.db_name = self._get_db_name_from_url(config.MONGO_DB_URL)

    def _get_db_name_from_url(self, mongo_url: str) -> str:
        """
        Извлекает имя базы данных из строки подключения MongoDB.
        Если имя базы данных не указано, используется значение из конфигурации.
        :param mongo_url: Строка подключения к MongoDB.
        :return: Имя базы данных.
        """
        try:
            # Разбираем строку подключения
            parsed_uri = parse_uri(mongo_url)
            # Извлекаем имя базы данных
            db_name = parsed_uri.get("database")
            
            # Если имя базы данных всё ещё не указано, используем значение по умолчанию
            if not db_name:
                db_name = "admin"  # База данных по умолчанию
            
            return db_name
        except Exception as e:
            raise ValueError(f"Ошибка при разборе строки подключения: {e}")

    def apply(self):
        """Устанавливает соединение с MongoDB."""
        self.client = MongoClient(config.MONGO_DB_URL)
        self.db = self.client[self.db_name]
        return self.db

    def close(self):
        """Закрывает соединение с MongoDB."""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None