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

