from app.factories.database_factory import DatabaseFactory
from app.db_connection.connection import Connection

# Создание зависимости для подключения к PostgreSQL
def get_postgres_session():
    connection = DatabaseFactory.create("pg")
    return connection.apply()
