from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.db_connection.connection import Connection
from app import config

# Основная база для SQLAlchemy
Base = declarative_base()

# Класс, который отвечает за соединение с PostgreSQL
class PostgresConnection(Connection):
    def __init__(self):
        self.engine = create_engine(config.POSTGRES_URL, pool_size=10, max_overflow=20)

    def apply(self):
        """Устанавливает соединение с PostgreSQL и возвращает сессию."""
        Session = sessionmaker(bind=self.engine)
        return Session()

    def close(self):
        """Закрытие соединения с базой данных."""
        self.engine.dispose()