from fastapi import APIRouter, HTTPException
from app.services.asistencia_service import registrar_asistencia, obtener_asistencias_semana, obtener_nombre_coleccion_semanal
from app.models.asistencia import AsistenciaCreate

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
    Obtiene todas las asistencias de la semana actual
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

