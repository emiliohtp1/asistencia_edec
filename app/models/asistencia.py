from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AsistenciaCreate(BaseModel):
    matricula: str
    tipo_registro: str  # "entrada" o "salida"

class AsistenciaDirectaCreate(BaseModel):
    """Modelo para crear asistencia directamente en la colección 'asistencia'"""
    matricula: str
    nombre_completo: str
    tipo_registro: str
    fecha: Optional[str] = None  # Si no se proporciona, se usa la fecha actual
    hora: Optional[str] = None  # Si no se proporciona, se usa la hora actual
    carrera: Optional[str] = None
    tipo_usuario: Optional[str] = None

class Asistencia(BaseModel):
    matricula: str
    nombre_completo: str
    tipo_registro: str
    fecha: str
    hora: str
    timestamp: datetime

