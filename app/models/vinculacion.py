"""
Modelos de datos para registros de vinculación del sistema EDEC.

Este módulo define los esquemas de validación (Pydantic) para:
- VinculacionCreate: Modelo para crear nuevos registros de vinculación
- VinculacionResponse: Respuesta con datos del registro de vinculación
- VinculacionDelete: Modelo para eliminar registros por teléfono
"""
from pydantic import BaseModel

class VinculacionCreate(BaseModel):
    nombre: str
    telefono: int
    programa: str

class VinculacionResponse(BaseModel):
    id: str
    nombre: str
    telefono: int
    programa: str
    fecha: str
    timestamp: str
