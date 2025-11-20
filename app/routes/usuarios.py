from fastapi import APIRouter, HTTPException
from app.services.usuario_service import obtener_usuario_por_matricula, obtener_todos_alumnos, obtener_todos_maestros
from app.models.usuario import UsuarioResponse
from typing import List

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])

@router.get("/{matricula}", response_model=UsuarioResponse)
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

@router.get("/alumnos/todos")
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

@router.get("/maestros/todos")
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

