from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AsistenciaCreate(BaseModel):
    matricula: str
    tipo_registro: str  # "entrada" o "salida"

class Asistencia(BaseModel):
    matricula: str
    nombre_completo: str
    tipo_registro: str
    fecha: str
    hora: str
    timestamp: datetime

