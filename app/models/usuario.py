"""
Modelos de datos para usuarios del sistema de asistencia EDEC.

Este módulo define los esquemas de validación (Pydantic) para:
- Usuario: Modelo base para usuarios (alumnos y maestros)
- UsuarioResponse: Respuesta al buscar un usuario por matrícula
- LoginRequest: Datos de autenticación (username y password)
- usuario_datos: Modelo completo con información detallada de alumnos
  (matrícula, nombre, coordinador, graduado, correo, campus, programa, ciclo, turno)
- UsuarioCreate: Modelo para crear nuevos usuarios en usuarios_apodaca
- UsuarioLogin: Modelo para autenticación de usuarios
- UsuarioResponseApodaca: Respuesta con datos del usuario autenticado
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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

# Modelos para usuarios de Apodaca
class UsuarioCreate(BaseModel):
    nombre_completo: str
    correo: str
    contraseña: str
    rol: str
    campus: str

class UsuarioLogin(BaseModel):
    correo: str
    contraseña: str

class UsuarioResponseApodaca(BaseModel):
    nombre_completo: str
    correo: str
    rol: str
    campus: str
    fecha_creacion: datetime

class UsuarioCambiarContraseña(BaseModel):
    correo: str
    contraseña_actual: str
    nueva_contraseña: str

# Modelos para fichados de Apodaca
class FichadoCreate(BaseModel):
    matricula: str
    nombre: str
    coordinador: str
    graduado: str
    correo: str
    campus: str
    programa: str
    ciclo: str
    turno: str