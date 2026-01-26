"""
Gestión de conexión a la base de datos MongoDB.

Este módulo maneja la conexión y desconexión de MongoDB usando PyMongo.
Proporciona una instancia singleton de la base de datos que se reutiliza
en toda la aplicación para evitar múltiples conexiones.
"""
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
    """Retorna la instancia de la base de datos principal"""
    return database.db

def get_db_usuarios():
    """Retorna la instancia de la base de datos de usuarios"""
    if database.client is None:
        connect_db()
    return database.client["usuarios_edec"]
