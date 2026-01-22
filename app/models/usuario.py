from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    matricula: str
    nombre_completo: str
    carrera: str
    tipo: str  # "alumno" o "maestro"

class UsuarioResponse(BaseModel):
    matricula: str
    nombre_completo: str
    carrera: str
    tipo: str
    encontrado: bool

class LoginRequest(BaseModel):
    username: str
    password: str

class usuario_datos(BaseModel):
    matricula: str
    nombre: str
    coordinador: str
    graduado: str
    correo: str
    campus: str
    programa: str
    ciclo: str
    turno: str