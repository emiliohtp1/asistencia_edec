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
    de la colección 'alumnos_bachillerato'
    """
    db = get_db()
    # Intentar buscar como string primero (formato más común en MongoDB)
    alumno = db.alumnos_bachillerato.find_one({"matricula": matricula})
    
    # Si no se encuentra, intentar como int
    if not alumno:
        try:
            matricula_int = int(matricula)
            alumno = db.alumnos_bachillerato.find_one({"matricula": matricula_int})
        except (ValueError, TypeError):
            pass
    
    if not alumno:
        return None
    
    # Convertir matrícula a int para el modelo
    matricula_valor = alumno["matricula"]
    if isinstance(matricula_valor, str):
        try:
            matricula_valor = int(matricula_valor)
        except (ValueError, TypeError):
            try:
                matricula_valor = int(matricula)
            except (ValueError, TypeError):
                # Si ambos fallan, usar el valor original
                pass
    
    return usuario_datos(
        matricula=matricula_valor,
        nombre=alumno["nombre"],
        coordinador=alumno["coordinador"],
        graduado=alumno["graduado"],
        correo=alumno["correo"],
        campus=alumno["campus"],
        programa=alumno["programa"],
        ciclo=alumno["ciclo"],
        turno=alumno["turno"]
    )

def obtener_datos_alumno_universidad(matricula: str) -> Optional[usuario_datos]:
    """
    Obtiene los datos de un alumno de universidad por su matrícula
    de la colección 'alumnos_universidad'
    """
    db = get_db()
    # Intentar buscar como string primero (formato más común en MongoDB)
    alumno = db.alumnos_universidad.find_one({"matricula": matricula})
    
    # Si no se encuentra, intentar como int
    if not alumno:
        try:
            matricula_int = int(matricula)
            alumno = db.alumnos_universidad.find_one({"matricula": matricula_int})
        except (ValueError, TypeError):
            pass
    
    if not alumno:
        return None
    
    # Convertir matrícula a int para el modelo
    matricula_valor = alumno["matricula"]
    if isinstance(matricula_valor, str):
        try:
            matricula_valor = int(matricula_valor)
        except (ValueError, TypeError):
            try:
                matricula_valor = int(matricula)
            except (ValueError, TypeError):
                # Si ambos fallan, usar el valor original
                pass
    
    return usuario_datos(
        matricula=matricula_valor,
        nombre=alumno["nombre"],
        coordinador=alumno["coordinador"],
        graduado=alumno["graduado"],
        correo=alumno["correo"],
        campus=alumno["campus"],
        programa=alumno["programa"],
        ciclo=alumno["ciclo"],
        turno=alumno["turno"]
    )