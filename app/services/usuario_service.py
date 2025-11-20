from app.database import get_db
from app.models.usuario import UsuarioResponse

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

