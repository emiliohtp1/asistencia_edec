"""
Servicios de lógica de negocio para operaciones con usuarios.

Este módulo contiene las funciones que interactúan con MongoDB para:
- Buscar usuarios (alumnos y maestros) por matrícula
- Obtener listas completas de alumnos y maestros
- Autenticar usuarios mediante credenciales
- Obtener datos detallados de alumnos de bachillerato y universidad
  (incluye mapeo de campos de MongoDB con mayúscula inicial al modelo)
"""
from app.database import get_db
from app.models.usuario import UsuarioResponse, usuario_datos
from typing import List, Dict, Optional

def obtener_usuario_por_matricula(matricula: str) -> UsuarioResponse:
    """
    Busca un usuario (alumno o maestro) por su matrícula
    """
    db = get_db()
    
    # Buscar primero en alumnos
    alumno = db.alumnos.find_one({"matricula": matricula})
    if alumno:
        return UsuarioResponse(
            matricula=alumno["matricula"],
            nombre_completo=alumno["nombre_completo"],
            carrera=alumno.get("carrera", "N/A"),
            tipo="alumno",
            encontrado=True
        )
    
    # Si no se encuentra, buscar en maestros
    maestro = db.maestros.find_one({"matricula": matricula})
    if maestro:
        return UsuarioResponse(
            matricula=maestro["matricula"],
            nombre_completo=maestro["nombre_completo"],
            carrera=maestro.get("carrera", "N/A"),
            tipo="maestro",
            encontrado=True
        )
    
    # Si no se encuentra en ninguno
    return UsuarioResponse(
        matricula=matricula,
        nombre_completo="",
        carrera="",
        tipo="",
        encontrado=False
    )

def obtener_todos_alumnos() -> List[Dict]:
    """
    Obtiene todos los alumnos de la colección 'alumnos'
    """
    db = get_db()
    alumnos = list(db.alumnos.find().sort("matricula", 1))
    
    # Convertir ObjectId a string y limpiar datos
    for alumno in alumnos:
        alumno["_id"] = str(alumno["_id"])
    
    return alumnos

def obtener_todos_maestros() -> List[Dict]:
    """
    Obtiene todos los maestros de la colección 'maestros'
    """
    db = get_db()
    maestros = list(db.maestros.find().sort("matricula", 1))
    
    # Convertir ObjectId a string y limpiar datos
    for maestro in maestros:
        maestro["_id"] = str(maestro["_id"])
    
    return maestros

def obtener_usuario_por_credenciales_db(username: str, password: str):
    """
    Busca un usuario en la colección 'login' por username y password.
    """
    db = get_db()
    coleccion = db.login

    usuario = coleccion.find_one({
        "username": username,
        "password": password
    })

    if not usuario:
        return None

    # Convertir _id a string
    usuario["_id"] = str(usuario["_id"])

    return usuario

def obtener_datos_alumno_bachillerato(matricula: str) -> Optional[usuario_datos]:
    """
    Obtiene los datos de un alumno de bachillerato por su matrícula
    de la colección 'alumnos_bachillerato_apodaca'
    """
    db = get_db()
    # Buscar por Matricula (con mayúscula) como string
    alumno = db.alumnos_bachillerato_apodaca.find_one({"Matricula": matricula})
    
    # Si no se encuentra, intentar como int
    if not alumno:
        try:
            matricula_int = int(matricula)
            alumno = db.alumnos_bachillerato_apodaca.find_one({"Matricula": matricula_int})
        except (ValueError, TypeError):
            pass
    
    if not alumno:
        return None
    
    # Mapear campos de MongoDB (con mayúscula) al modelo (minúscula)
    # La matrícula se mantiene como string según el modelo
    matricula_valor = str(alumno.get("Matricula", matricula))
    
    return usuario_datos(
        matricula=matricula_valor,
        nombre=alumno.get("Nombre", ""),
        coordinador=alumno.get("Coordinador", ""),
        graduado=alumno.get("Graduado", ""),
        correo=alumno.get("Correo", ""),
        campus=alumno.get("Campus", ""),
        programa=alumno.get("Programa", ""),
        ciclo=alumno.get("Ciclo", ""),
        turno=alumno.get("Turno", "")
    )

def obtener_datos_alumno_universidad(matricula: str) -> Optional[usuario_datos]:
    """
    Obtiene los datos de un alumno de universidad por su matrícula
    de la colección 'alumnos_universidad_apodaca'
    """
    db = get_db()
    # Buscar por Matricula (con mayúscula) como string
    alumno = db.alumnos_universidad_apodaca.find_one({"Matricula": matricula})
    
    # Si no se encuentra, intentar como int
    if not alumno:
        try:
            matricula_int = int(matricula)
            alumno = db.alumnos_universidad_apodaca.find_one({"Matricula": matricula_int})
        except (ValueError, TypeError):
            pass
    
    if not alumno:
        return None
    
    # Mapear campos de MongoDB (con mayúscula) al modelo (minúscula)
    # La matrícula se mantiene como string según el modelo
    matricula_valor = str(alumno.get("Matricula", matricula))
    
    return usuario_datos(
        matricula=matricula_valor,
        nombre=alumno.get("Nombre", ""),
        coordinador=alumno.get("Coordinador", ""),
        graduado=alumno.get("Graduado", ""),
        correo=alumno.get("Correo", ""),
        campus=alumno.get("Campus", ""),
        programa=alumno.get("Programa", ""),
        ciclo=alumno.get("Ciclo", ""),
        turno=alumno.get("Turno", "")
    )

def obtener_todos_alumnos_bachillerato() -> List[usuario_datos]:
    """
    Obtiene todos los alumnos de bachillerato de la colección 'alumnos_bachillerato'
    """
    db = get_db()
    alumnos_raw = list(db.alumnos_bachillerato_apodaca.find().sort("Matricula", 1))
    
    alumnos = []
    for alumno_raw in alumnos_raw:
        # Mapear campos de MongoDB (con mayúscula) al modelo (minúscula)
        matricula_valor = str(alumno_raw.get("Matricula", ""))
        
        alumno = usuario_datos(
            matricula=matricula_valor,
            nombre=alumno_raw.get("Nombre", ""),
            coordinador=alumno_raw.get("Coordinador", ""),
            graduado=alumno_raw.get("Graduado", ""),
            correo=alumno_raw.get("Correo", ""),
            campus=alumno_raw.get("Campus", ""),
            programa=alumno_raw.get("Programa", ""),
            ciclo=alumno_raw.get("Ciclo", ""),
            turno=alumno_raw.get("Turno", "")
        )
        alumnos.append(alumno)
    
    return alumnos

def obtener_todos_alumnos_universidad() -> List[usuario_datos]:
    """
    Obtiene todos los alumnos de universidad de la colección 'alumnos_universidad_apodaca'
    """
    db = get_db()
    alumnos_raw = list(db.alumnos_universidad_apodaca.find().sort("Matricula", 1))
    
    alumnos = []
    for alumno_raw in alumnos_raw:
        # Mapear campos de MongoDB (con mayúscula) al modelo (minúscula)
        matricula_valor = str(alumno_raw.get("Matricula", ""))
        
        alumno = usuario_datos(
            matricula=matricula_valor,
            nombre=alumno_raw.get("Nombre", ""),
            coordinador=alumno_raw.get("Coordinador", ""),
            graduado=alumno_raw.get("Graduado", ""),
            correo=alumno_raw.get("Correo", ""),
            campus=alumno_raw.get("Campus", ""),
            programa=alumno_raw.get("Programa", ""),
            ciclo=alumno_raw.get("Ciclo", ""),
            turno=alumno_raw.get("Turno", "")
        )
        alumnos.append(alumno)
    
    return alumnos