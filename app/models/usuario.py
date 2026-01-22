"""
Modelos de datos para usuarios del sistema de asistencia EDEC.

Este módulo define los esquemas de validación (Pydantic) para:
- Usuario: Modelo base para usuarios (alumnos y maestros)
- UsuarioResponse: Respuesta al buscar un usuario por matrícula
- LoginRequest: Datos de autenticación (username y password)
- usuario_datos: Modelo completo con información detallada de alumnos
  (matrícula, nombre, coordinador, graduado, correo, campus, programa, ciclo, turno)
"""
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