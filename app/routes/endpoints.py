"""
Endpoints de la API REST para el sistema de asistencia EDEC.

Este módulo define todas las rutas HTTP de la API, organizadas en:
- Endpoints de usuarios: búsqueda de alumnos y maestros
- Endpoints de alumnos: datos detallados de bachillerato y universidad
- Endpoints de asistencias: registro y consulta de asistencias
- Endpoints de autenticación: login de usuarios

Las rutas están organizadas con tags para documentación automática en Swagger/OpenAPI.
"""
from fastapi import APIRouter, HTTPException
from app.services.usuario_service import (
    obtener_usuario_por_matricula,
    obtener_usuario_por_credenciales_db,
    obtener_todos_alumnos,
    obtener_todos_maestros,
    obtener_datos_alumno_bachillerato,
    obtener_datos_alumno_universidad,
    obtener_todos_alumnos_bachillerato,
    obtener_todos_alumnos_universidad
)
from app.services.asistencia_service import (
    registrar_asistencia, 
    obtener_todas_asistencias,
    obtener_asistencias_por_matricula,
)
from app.models.usuario import UsuarioResponse, LoginRequest, usuario_datos
from app.models.asistencia import AsistenciaCreate

# Router principal
router = APIRouter()

# ============================================================================
# ENDPOINTS DE USUARIOS
# ============================================================================



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

@router.get("/api/alumnos/bachillerato", tags=["alumnos"])
async def obtener_todos_alumnos_bachillerato_endpoint():
    """
    Obtiene todos los alumnos de bachillerato de la colección 'alumnos_bachillerato'
    """
    try:
        alumnos = obtener_todos_alumnos_bachillerato()
        return {
            "total": len(alumnos),
            "alumnos": alumnos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/alumnos/universidad", tags=["alumnos"])
async def obtener_todos_alumnos_universidad_endpoint():
    """
    Obtiene todos los alumnos de universidad de la colección 'alumnos_universidad'
    """
    try:
        alumnos = obtener_todos_alumnos_universidad()
        return {
            "total": len(alumnos),
            "alumnos": alumnos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/alumnos/bachillerato/{matricula}", response_model=usuario_datos, tags=["alumnos"])
async def obtener_alumno_bachillerato(matricula: str):
    """
    Obtiene los datos de un alumno de bachillerato por su matrícula
    de la colección 'alumnos_bachillerato'
    """
    try:
        alumno = obtener_datos_alumno_bachillerato(matricula)
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        return alumno
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/alumnos/universidad/{matricula}", response_model=usuario_datos, tags=["alumnos"])
async def obtener_alumno_universidad(matricula: str):
    """
    Obtiene los datos de un alumno de universidad por su matrícula
    de la colección 'alumnos_universidad'
    """
    try:
        alumno = obtener_datos_alumno_universidad(matricula)
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        return alumno
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ENDPOINTS DE ASISTENCIAS
# ============================================================================

@router.post("/api/asistencias/registrar", tags=["asistencias"])
async def crear_registro_asistencia(asistencia: dict):
    """
    Registra la asistencia de entrada de una matrícula.
    Solo permite un registro por matrícula por día.
    Guarda: Matricula, Nombre, Fecha (DD/MM/YYYY), Hora (HH:MM) en horario de México.
    Almacena en la colección 'asistencia_general_apodaca'.
    """
    try:
        if "matricula" not in asistencia:
            raise HTTPException(status_code=400, detail="La matrícula es requerida")
        
        if "nombre" not in asistencia:
            raise HTTPException(status_code=400, detail="El nombre es requerido")
        
        resultado = registrar_asistencia(
            matricula=asistencia["matricula"],
            nombre=asistencia["nombre"]
        )
        return resultado

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/api/asistencias/matricula/{matricula}", tags=["asistencias"])
async def obtener_asistencias_por_matricula_endpoint(matricula: str):
    """
    Obtiene todos los registros de asistencia de una matrícula específica
    """
    try:
        asistencias = obtener_asistencias_por_matricula(matricula)
        return {
            "matricula": matricula,
            "total": len(asistencias),
            "asistencias": asistencias
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/asistencias/todas", tags=["asistencias"])
async def obtener_todas_las_asistencias():
    """
    Obtiene todos los registros de la colección 'asistencia_general'
    """
    try:
        asistencias = obtener_todas_asistencias()
        return {
            "coleccion": "asistencia_general",
            "total": len(asistencias),
            "asistencias": asistencias
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/usuarios/login", tags=["login"])
async def login_usuario(datos: LoginRequest):
    """
    Verifica credenciales de un usuario en la colección 'login'
    """
    try:
        usuario = obtener_usuario_por_credenciales_db(
            datos.username,
            datos.password
        )

        if not usuario:
            raise HTTPException(
                status_code=401,
                detail="Credenciales incorrectas"
            )

        return {
            "mensaje": "Login exitoso",
            "usuario": usuario
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en el servidor al intentar login: {e}")
        raise HTTPException(status_code=500, detail=str(e))