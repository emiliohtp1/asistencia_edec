from fastapi import APIRouter, HTTPException
from app.services.usuario_service import obtener_usuario_por_matricula
from app.models.usuario import UsuarioResponse

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

