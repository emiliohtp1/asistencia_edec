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
    obtener_todos_alumnos_universidad,
    crear_usuario_apodaca,
    autenticar_usuario_apodaca,
    cambiar_contraseña_usuario_apodaca,
    obtener_todos_usuarios_apodaca,
    obtener_usuario_por_correo_apodaca,
    eliminar_usuario_por_correo_apodaca
)
from app.services.asistencia_service import (
    registrar_asistencia, 
    obtener_todas_asistencias,
    obtener_asistencias_por_matricula,
    obtener_todas_asistencias_apodaca,
    obtener_asistencias_apodaca_por_matricula,
    registrar_fichado_apodaca,
    obtener_fichados_apodaca_agrupados
)
from app.models.usuario import UsuarioResponse, LoginRequest, usuario_datos, UsuarioCreate, UsuarioLogin, UsuarioResponseApodaca, UsuarioCambiarContraseña, FichadoCreate
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

@router.get("/api/asistencias/apodaca/todas", tags=["asistencias"])
async def obtener_todas_las_asistencias_apodaca():
    """
    Obtiene todos los registros de asistencia de la colección 'asistencia_general_apodaca'
    """
    try:
        asistencias = obtener_todas_asistencias_apodaca()
        return {
            "coleccion": "asistencia_general_apodaca",
            "total": len(asistencias),
            "asistencias": asistencias
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/asistencias/apodaca/{matricula}", tags=["asistencias"])
async def obtener_asistencias_apodaca_por_matricula_endpoint(matricula: str):
    """
    Obtiene todos los registros de asistencia de una matrícula específica
    de la colección 'asistencia_general_apodaca'
    """
    try:
        asistencias = obtener_asistencias_apodaca_por_matricula(matricula)
        return {
            "matricula": matricula,
            "coleccion": "asistencia_general_apodaca",
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

# ============================================================================
# ENDPOINTS PARA USUARIOS DE APODACA (Base de datos usuarios_edec)
# ============================================================================

@router.post("/api/usuarios/apodaca/crear", tags=["usuarios_apodaca"])
async def crear_usuario(usuario: UsuarioCreate):
    """
    Crea un nuevo usuario en la base de datos usuarios_edec, colección usuarios_apodaca.
    La contraseña se hashea automáticamente antes de guardarse.
    """
    try:
        nuevo_usuario = crear_usuario_apodaca(usuario)
        return {
            "mensaje": "Usuario creado exitosamente",
            "usuario": nuevo_usuario
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

@router.post("/api/usuarios/apodaca/login", tags=["usuarios_apodaca"])
async def login_usuario_apodaca(datos: UsuarioLogin):
    """
    Autentica un usuario en la base de datos usuarios_edec, colección usuarios_apodaca.
    Verifica el correo y contraseña (hasheada).
    """
    try:
        usuario = autenticar_usuario_apodaca(
            datos.correo,
            datos.contraseña
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

@router.post("/api/usuarios/apodaca/cambiar-contraseña", tags=["usuarios_apodaca"])
async def cambiar_contraseña(datos: UsuarioCambiarContraseña):
    """
    Cambia la contraseña de un usuario en la base de datos usuarios_edec.
    Requiere validar la contraseña actual antes de cambiarla por la nueva.
    """
    try:
        resultado = cambiar_contraseña_usuario_apodaca(datos)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error al cambiar contraseña: {e}")
        raise HTTPException(status_code=500, detail=f"Error al cambiar contraseña: {str(e)}")

@router.get("/api/usuarios/apodaca", tags=["usuarios_apodaca"])
async def obtener_todos_usuarios():
    """
    Obtiene todos los usuarios de la base de datos usuarios_edec, colección usuarios_apodaca.
    Retorna todos los datos excepto las contraseñas.
    """
    try:
        usuarios = obtener_todos_usuarios_apodaca()
        return {
            "total": len(usuarios),
            "usuarios": usuarios
        }
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

@router.get("/api/usuarios/apodaca/{correo}", tags=["usuarios_apodaca"])
async def obtener_usuario_por_correo(correo: str):
    """
    Obtiene un usuario específico por su correo electrónico.
    Retorna todos los datos del usuario excepto la contraseña.
    """
    try:
        usuario = obtener_usuario_por_correo_apodaca(correo)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al obtener usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {str(e)}")

@router.delete("/api/usuarios/apodaca/{correo}", tags=["usuarios_apodaca"])
async def eliminar_usuario(correo: str):
    """
    Elimina un usuario de la base de datos usuarios_edec por su correo electrónico.
    Retorna información sobre el usuario eliminado.
    """
    try:
        resultado = eliminar_usuario_por_correo_apodaca(correo)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {str(e)}")

# ============================================================================
# ENDPOINTS PARA FICHADOS DE APODACA (Base de datos asistencia_edec)
# ============================================================================

@router.post("/api/fichados/apodaca/registrar", tags=["fichados_apodaca"])
async def registrar_fichado(fichado: FichadoCreate):
    """
    Registra un fichado en la base de datos asistencia_edec, colección fichados_apodaca.
    Agrega automáticamente la fecha_registro_ficha con fecha y hora actual.
    """
    try:
        fichado_dict = fichado.model_dump()
        resultado = registrar_fichado_apodaca(fichado_dict)
        return {
            "mensaje": "Fichado registrado exitosamente",
            "fichado": resultado
        }
    except Exception as e:
        print(f"Error al registrar fichado: {e}")
        raise HTTPException(status_code=500, detail=f"Error al registrar fichado: {str(e)}")

@router.get("/api/fichados/apodaca", tags=["fichados_apodaca"])
async def obtener_fichados_agrupados():
    """
    Obtiene todos los fichados de la colección fichados_apodaca.
    Si existen varios objetos con el mismo nombre y matricula, muestra solo uno
    con un campo cantidad_fichas que indica cuántas veces se repite.
    """
    try:
        fichados = obtener_fichados_apodaca_agrupados()
        return {
            "total": len(fichados),
            "fichados": fichados
        }
    except Exception as e:
        print(f"Error al obtener fichados: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener fichados: {str(e)}")