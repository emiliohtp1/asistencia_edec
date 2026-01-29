"""
Servicios de lógica de negocio para operaciones con usuarios.

Este módulo contiene las funciones que interactúan con MongoDB para:
- Buscar usuarios (alumnos y maestros) por matrícula
- Obtener listas completas de alumnos y maestros
- Autenticar usuarios mediante credenciales
- Obtener datos detallados de alumnos de bachillerato y universidad
  (incluye mapeo de campos de MongoDB con mayúscula inicial al modelo)
- Crear y autenticar usuarios en la base de datos usuarios_edec
"""
from app.database import get_db, get_db_usuarios
from app.models.usuario import UsuarioResponse, usuario_datos, UsuarioCreate, UsuarioResponseApodaca, UsuarioCambiarContraseña
from typing import List, Dict, Optional
from datetime import datetime
import bcrypt

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

# ============================================================================
# FUNCIONES PARA USUARIOS DE APODACA (Base de datos usuarios_edec)
# ============================================================================

def crear_usuario_apodaca(usuario: UsuarioCreate) -> Dict:
    """
    Crea un nuevo usuario en la base de datos usuarios_edec, colección usuarios_apodaca.
    Hashea la contraseña antes de guardarla.
    """
    db = get_db_usuarios()
    coleccion = db.usuarios_apodaca
    
    # Verificar si el correo ya existe
    usuario_existente = coleccion.find_one({"correo": usuario.correo})
    if usuario_existente:
        raise ValueError(f"El correo '{usuario.correo}' ya está en uso")
    
    # Hashear la contraseña
    contraseña_hasheada = bcrypt.hashpw(
        usuario.contraseña.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # Crear el documento del usuario
    nuevo_usuario = {
        "nombre_completo": usuario.nombre_completo,
        "correo": usuario.correo,
        "contraseña": contraseña_hasheada,
        "rol": usuario.rol,
        "campus": usuario.campus,
        "fecha_creacion": datetime.now()
    }
    
    # Insertar en la base de datos
    resultado = coleccion.insert_one(nuevo_usuario)
    
    # Retornar el usuario creado (sin la contraseña)
    nuevo_usuario["_id"] = str(resultado.inserted_id)
    nuevo_usuario.pop("contraseña", None)
    
    return nuevo_usuario

def autenticar_usuario_apodaca(correo: str, contraseña: str) -> Optional[UsuarioResponseApodaca]:
    """
    Autentica un usuario verificando el correo y contraseña.
    Retorna los datos del usuario si las credenciales son correctas, None en caso contrario.
    """
    db = get_db_usuarios()
    coleccion = db.usuarios_apodaca
    
    # Buscar el usuario por correo
    usuario = coleccion.find_one({"correo": correo})
    
    if not usuario:
        return None
    
    # Verificar la contraseña
    contraseña_hasheada = usuario.get("contraseña", "")
    if not bcrypt.checkpw(
        contraseña.encode('utf-8'),
        contraseña_hasheada.encode('utf-8')
    ):
        return None
    
    # Retornar los datos del usuario (sin la contraseña)
    return UsuarioResponseApodaca(
        nombre_completo=usuario.get("nombre_completo", ""),
        correo=usuario.get("correo", ""),
        rol=usuario.get("rol", ""),
        campus=usuario.get("campus", ""),
        fecha_creacion=usuario.get("fecha_creacion", datetime.now())
    )

def cambiar_contraseña_usuario_apodaca(datos: UsuarioCambiarContraseña) -> Dict:
    """
    Cambia la contraseña de un usuario en la base de datos usuarios_edec.
    Valida que la contraseña actual sea correcta antes de cambiarla.
    """
    db = get_db_usuarios()
    coleccion = db.usuarios_apodaca
    
    # Buscar el usuario por correo
    usuario = coleccion.find_one({"correo": datos.correo})
    
    if not usuario:
        raise ValueError("Usuario no encontrado")
    
    # Verificar que la contraseña actual sea correcta
    contraseña_hasheada_actual = usuario.get("contraseña", "")
    if not bcrypt.checkpw(
        datos.contraseña_actual.encode('utf-8'),
        contraseña_hasheada_actual.encode('utf-8')
    ):
        raise ValueError("La contraseña actual es incorrecta")
    
    # Hashear la nueva contraseña
    nueva_contraseña_hasheada = bcrypt.hashpw(
        datos.nueva_contraseña.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # Actualizar la contraseña en la base de datos
    resultado = coleccion.update_one(
        {"correo": datos.correo},
        {"$set": {"contraseña": nueva_contraseña_hasheada}}
    )
    
    if resultado.modified_count == 0:
        raise ValueError("No se pudo actualizar la contraseña")
    
    return {
        "mensaje": "Contraseña actualizada exitosamente",
        "correo": datos.correo
    }

def obtener_todos_usuarios_apodaca() -> List[Dict]:
    """
    Obtiene todos los usuarios de la base de datos usuarios_edec, colección usuarios_apodaca.
    Retorna todos los datos excepto la contraseña.
    """
    db = get_db_usuarios()
    coleccion = db.usuarios_apodaca
    
    usuarios = list(coleccion.find().sort("fecha_creacion", -1))
    
    # Convertir ObjectId a string y eliminar contraseñas
    for usuario in usuarios:
        usuario["_id"] = str(usuario["_id"])
        usuario.pop("contraseña", None)
    
    return usuarios

def obtener_usuario_por_correo_apodaca(correo: str) -> Optional[Dict]:
    """
    Obtiene un usuario por su correo de la base de datos usuarios_edec.
    Retorna todos los datos excepto la contraseña.
    """
    db = get_db_usuarios()
    coleccion = db.usuarios_apodaca
    
    usuario = coleccion.find_one({"correo": correo})
    
    if not usuario:
        return None
    
    # Convertir ObjectId a string y eliminar contraseña
    usuario["_id"] = str(usuario["_id"])
    usuario.pop("contraseña", None)
    
    return usuario

def eliminar_usuario_por_correo_apodaca(correo: str) -> Dict:
    """
    Elimina un usuario de la base de datos usuarios_edec por su correo.
    Retorna información sobre el usuario eliminado.
    """
    db = get_db_usuarios()
    coleccion = db.usuarios_apodaca
    
    # Verificar si el usuario existe
    usuario = coleccion.find_one({"correo": correo})
    if not usuario:
        raise ValueError("Usuario no encontrado")
    
    # Eliminar el usuario
    resultado = coleccion.delete_one({"correo": correo})
    
    if resultado.deleted_count == 0:
        raise ValueError("No se pudo eliminar el usuario")
    
    # Retornar información del usuario eliminado (sin la contraseña)
    usuario["_id"] = str(usuario["_id"])
    usuario.pop("contraseña", None)
    
    return {
        "mensaje": "Usuario eliminado exitosamente",
        "usuario_eliminado": usuario
    }

# ============================================================================
# FUNCIONES PARA GESTIÓN DE ALUMNOS (Bachillerato y Universidad)
# ============================================================================

def crear_alumno_bachillerato(alumno: usuario_datos) -> Dict:
    """
    Crea un nuevo alumno en la colección 'alumnos_bachillerato_apodaca'.
    Los campos se guardan con mayúscula inicial para mantener consistencia con MongoDB.
    """
    db = get_db()
    coleccion = db.alumnos_bachillerato_apodaca
    
    # Verificar si la matrícula ya existe
    matricula_existente = coleccion.find_one({"Matricula": alumno.matricula})
    if matricula_existente:
        raise ValueError(f"La matrícula '{alumno.matricula}' ya existe en bachillerato")
    
    # Crear el documento del alumno con campos en mayúscula (formato MongoDB)
    nuevo_alumno = {
        "Matricula": alumno.matricula,
        "Nombre": alumno.nombre,
        "Coordinador": alumno.coordinador,
        "Graduado": alumno.graduado,
        "Correo": alumno.correo,
        "Campus": alumno.campus,
        "Programa": alumno.programa,
        "Ciclo": alumno.ciclo,
        "Turno": alumno.turno
    }
    
    # Insertar en la base de datos
    resultado = coleccion.insert_one(nuevo_alumno)
    
    # Retornar el alumno creado
    nuevo_alumno["_id"] = str(resultado.inserted_id)
    
    return nuevo_alumno

def crear_alumno_universidad(alumno: usuario_datos) -> Dict:
    """
    Crea un nuevo alumno en la colección 'alumnos_universidad_apodaca'.
    Los campos se guardan con mayúscula inicial para mantener consistencia con MongoDB.
    """
    db = get_db()
    coleccion = db.alumnos_universidad_apodaca
    
    # Verificar si la matrícula ya existe
    matricula_existente = coleccion.find_one({"Matricula": alumno.matricula})
    if matricula_existente:
        raise ValueError(f"La matrícula '{alumno.matricula}' ya existe en universidad")
    
    # Crear el documento del alumno con campos en mayúscula (formato MongoDB)
    nuevo_alumno = {
        "Matricula": alumno.matricula,
        "Nombre": alumno.nombre,
        "Coordinador": alumno.coordinador,
        "Graduado": alumno.graduado,
        "Correo": alumno.correo,
        "Campus": alumno.campus,
        "Programa": alumno.programa,
        "Ciclo": alumno.ciclo,
        "Turno": alumno.turno
    }
    
    # Insertar en la base de datos
    resultado = coleccion.insert_one(nuevo_alumno)
    
    # Retornar el alumno creado
    nuevo_alumno["_id"] = str(resultado.inserted_id)
    
    return nuevo_alumno

def eliminar_alumno_bachillerato(matricula: str) -> Dict:
    """
    Elimina un alumno de la colección 'alumnos_bachillerato_apodaca' por su matrícula.
    Retorna información sobre el alumno eliminado.
    """
    db = get_db()
    coleccion = db.alumnos_bachillerato_apodaca
    
    # Buscar el alumno por matrícula (intentar como string e int)
    alumno = coleccion.find_one({"Matricula": matricula})
    if not alumno:
        try:
            matricula_int = int(matricula)
            alumno = coleccion.find_one({"Matricula": matricula_int})
        except (ValueError, TypeError):
            pass
    
    if not alumno:
        raise ValueError("Alumno no encontrado en bachillerato")
    
    # Eliminar el alumno
    resultado = coleccion.delete_one({"Matricula": alumno.get("Matricula")})
    
    if resultado.deleted_count == 0:
        raise ValueError("No se pudo eliminar el alumno")
    
    # Retornar información del alumno eliminado
    alumno["_id"] = str(alumno["_id"])
    
    return {
        "mensaje": "Alumno eliminado exitosamente de bachillerato",
        "alumno_eliminado": alumno
    }

def eliminar_alumno_universidad(matricula: str) -> Dict:
    """
    Elimina un alumno de la colección 'alumnos_universidad_apodaca' por su matrícula.
    Retorna información sobre el alumno eliminado.
    """
    db = get_db()
    coleccion = db.alumnos_universidad_apodaca
    
    # Buscar el alumno por matrícula (intentar como string e int)
    alumno = coleccion.find_one({"Matricula": matricula})
    if not alumno:
        try:
            matricula_int = int(matricula)
            alumno = coleccion.find_one({"Matricula": matricula_int})
        except (ValueError, TypeError):
            pass
    
    if not alumno:
        raise ValueError("Alumno no encontrado en universidad")
    
    # Eliminar el alumno
    resultado = coleccion.delete_one({"Matricula": alumno.get("Matricula")})
    
    if resultado.deleted_count == 0:
        raise ValueError("No se pudo eliminar el alumno")
    
    # Retornar información del alumno eliminado
    alumno["_id"] = str(alumno["_id"])
    
    return {
        "mensaje": "Alumno eliminado exitosamente de universidad",
        "alumno_eliminado": alumno
    }