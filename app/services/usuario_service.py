from app.database import get_db
from app.models.usuario import UsuarioResponse
from typing import List, Dict

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