import mongoengine as me
from app.db_connection.connection import Connection
from app import config

# Класс, который отвечает за соединение с MongoDB
class MongoConnection(Connection):
    def __init__(self):
        # Используем имя базы данных из конфигурационного файла
        self.db_name = config.MONGO_DB_NAME

    def apply(self):
        """Устанавливает соединение с MongoDB."""
        me.connect(self.db_name, host='localhost', port=27017)