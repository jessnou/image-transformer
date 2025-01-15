from app.factories.database_factory import DatabaseFactory

# Создание зависимости для подключения к PostgreSQL
def get_postgres_session():
    connection = DatabaseFactory.create("pg")
    return connection.apply()

# Создание зависимости для подключения к Mongo
def get_mongo_db():
    mongo_connection = DatabaseFactory.create('mongo')
    return mongo_connection.apply()