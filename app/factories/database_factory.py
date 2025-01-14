# Фабрика для создания подключения
from sqlalchemy import Connection
from app.db_connection.mongo import MongoConnection
from app.db_connection.pg import PostgresConnection


class DatabaseFactory:
    @staticmethod
    def create(type: str) -> Connection:
        if type == "pg":
            return PostgresConnection()
        elif type == "mongo":
            return MongoConnection()
        else:
            raise ValueError(f"Unsupported database type: {type}")
        
