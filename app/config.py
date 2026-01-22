"""
Configuración de la aplicación mediante variables de entorno.

Este módulo carga las variables de entorno desde un archivo .env y define
la clase Config con todos los parámetros necesarios para la aplicación:
- MONGODB_URI: URI de conexión a MongoDB (desde Render.com o local)
- DATABASE_NAME: Nombre de la base de datos
- HOST y PORT: Configuración del servidor
- EXCEL_DIR: Directorio para reportes Excel
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "asistencia_edec")
    HOST = os.getenv("HOST", "0.0.0.0")
    # Render.com proporciona PORT automáticamente, usar 8000 como fallback
    PORT = int(os.getenv("PORT", 8000))
    EXCEL_DIR = os.getenv("EXCEL_DIR", "./excel_reports")

