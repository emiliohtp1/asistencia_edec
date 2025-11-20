from pymongo import MongoClient
from app.config import Config

class Database:
    client: MongoClient = None
    db = None

database = Database()

def connect_db():
    """Conecta a la base de datos MongoDB"""
    database.client = MongoClient(Config.MONGODB_URI)
    database.db = database.client[Config.DATABASE_NAME]
    print("✅ Conectado a MongoDB")

def close_db():
    """Cierra la conexión a la base de datos"""
    if database.client:
        database.client.close()
        print("❌ Desconectado de MongoDB")

def get_db():
    """Retorna la instancia de la base de datos"""
    return database.db

