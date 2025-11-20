from fastapi import APIRouter, HTTPException
from app.services.asistencia_service import (
    registrar_asistencia, 
    obtener_asistencias_semana, 
    obtener_nombre_coleccion_semanal,
    obtener_todas_asistencias,
    crear_asistencia_directa
)
from app.models.asistencia import AsistenciaCreate, AsistenciaDirectaCreate

router = APIRouter(prefix="/api/asistencias", tags=["asistencias"])

@router.post("/registrar")
async def crear_registro_asistencia(asistencia: AsistenciaCreate):
    """
    Registra una nueva asistencia (entrada o salida)
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

@router.get("/semana-actual")
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

@router.get("/todas")
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

@router.post("/crear")
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

