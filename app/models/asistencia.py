from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AsistenciaCreate(BaseModel):
    """Modelo para crear un registro de asistencia"""
    matricula: str

class Asistencia(BaseModel):
    """Modelo de respuesta para un registro de asistencia"""
    matricula: str
    fecha: str  # Formato: DD/MM/YYYY
    hora: str  # Formato: HH:MM
    timestamp: datetime

