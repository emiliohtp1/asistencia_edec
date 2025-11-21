"""
Archivo único con todos los endpoints de la API
"""
from fastapi import APIRouter, HTTPException
from app.services.usuario_service import obtener_usuario_por_matricula, obtener_todos_alumnos, obtener_todos_maestros
from app.services.asistencia_service import (
    registrar_asistencia, 
    obtener_asistencias_semana, 
    obtener_nombre_coleccion_semanal,
    obtener_todas_asistencias,
    crear_asistencia_directa,
    obtener_todos_usuarios_login
)
from app.models.usuario import UsuarioResponse
from app.models.asistencia import AsistenciaCreate, AsistenciaDirectaCreate

# Router principal
router = APIRouter()

# ============================================================================
# ENDPOINTS DE USUARIOS
# ============================================================================

@router.get("/api/usuarios/{matricula}", response_model=UsuarioResponse, tags=["usuarios"])
async def obtener_usuario(matricula: str):
    """
    Obtiene la información de un usuario (alumno o maestro) por su matrícula
    """
    try:
        usuario = obtener_usuario_por_matricula(matricula)
        if not usuario.encontrado:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/usuarios/alumnos/todos", tags=["usuarios"])
async def obtener_alumnos():
    """
    Obtiene todos los alumnos de la colección 'alumnos'
    """
    try:
        alumnos = obtener_todos_alumnos()
        return {
            "total": len(alumnos),
            "alumnos": alumnos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/usuarios/maestros/todos", tags=["usuarios"])
async def obtener_maestros():
    """
    Obtiene todos los maestros de la colección 'maestros'
    """
    try:
        maestros = obtener_todos_maestros()
        return {
            "total": len(maestros),
            "maestros": maestros
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ENDPOINTS DE ASISTENCIAS
# ============================================================================

@router.post("/api/asistencias/registrar", tags=["asistencias"])
async def crear_registro_asistencia(asistencia: AsistenciaCreate):
    """
    Registra una nueva asistencia (entrada o salida) en colecciones semanales
    """
    try:
        if asistencia.tipo_registro not in ["entrada", "salida"]:
            raise HTTPException(
                status_code=400, 
                detail="El tipo_registro debe ser 'entrada' o 'salida'"
            )
        
        resultado = registrar_asistencia(
            matricula=asistencia.matricula,
            tipo_registro=asistencia.tipo_registro
        )
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/asistencias/semana-actual", tags=["asistencias"])
async def obtener_asistencias_semana_actual():
    """
    Obtiene todas las asistencias de la semana actual (colecciones semanales)
    """
    try:
        nombre_coleccion = obtener_nombre_coleccion_semanal()
        asistencias = obtener_asistencias_semana(nombre_coleccion)
        return {
            "coleccion": nombre_coleccion,
            "total": len(asistencias),
            "asistencias": asistencias
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/asistencias/todas", tags=["asistencias"])
async def obtener_todas_las_asistencias():
    """
    Obtiene todos los registros de la colección 'asistencia'
    """
    try:
        asistencias = obtener_todas_asistencias()
        return {
            "coleccion": "asistencia",
            "total": len(asistencias),
            "asistencias": asistencias
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/asistencias/crear", tags=["asistencias"])
async def crear_asistencia_directa_endpoint(asistencia: AsistenciaDirectaCreate):
    """
    Crea un registro de asistencia directamente en la colección 'asistencia'
    """
    try:
        # Validar tipo_registro
        if asistencia.tipo_registro not in ["entrada", "salida"]:
            raise HTTPException(
                status_code=400,
                detail="El tipo_registro debe ser 'entrada' o 'salida'"
            )
        
        # Convertir el modelo a diccionario
        datos = asistencia.dict()
        
        # Crear la asistencia
        resultado = crear_asistencia_directa(datos)
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/usuarios/login/todos", tags=["login"])
async def obtener_todos_usuarios():
    """
    Obtiene todos los usuarios de la colección 'login'
    """
    try:
        # ⚠️ CORRECCIÓN CLAVE: Llama a la función de la BD, NO a sí misma
        usuarios = obtener_todos_usuarios_login() 
        
        return {
            "login": usuarios
        }
        
    except Exception as e:
        # Si ocurre un error en la BD, lanza un error 500
        raise HTTPException(status_code=500, detail=str(e))