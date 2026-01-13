from datetime import datetime
from app.database import get_db
from typing import List, Dict
import pytz

def obtener_hora_mexico():
    """
    Obtiene la fecha y hora actual en horario de México (UTC-6)
    """
    zona_mexico = pytz.timezone('America/Mexico_City')
    ahora_mexico = datetime.now(zona_mexico)
    return ahora_mexico

def registrar_asistencia(matricula: str) -> dict:
    """
    Registra la asistencia de entrada de una matrícula.
    - Solo permite un registro por matrícula por día
    - Guarda: matrícula, fecha (DD/MM/YYYY), hora (HH:MM)
    - Almacena en la colección 'asistencia_general'
    """

    db = get_db()
    coleccion = db.asistencia_general

    # Obtener fecha y hora en horario de México
    ahora_mexico = obtener_hora_mexico()
    fecha_formato = ahora_mexico.strftime("%d/%m/%Y")
    hora_formato = ahora_mexico.strftime("%H:%M")

    # Verificar si ya existe un registro para esta matrícula hoy
    registro_existente = coleccion.find_one({
        "matricula": matricula,
        "fecha": fecha_formato
    })

    if registro_existente:
        raise ValueError(f"La matrícula {matricula} ya tiene un registro de asistencia para hoy ({fecha_formato})")

    # Crear el registro
    registro = {
        "matricula": matricula,
        "fecha": fecha_formato,
        "hora": hora_formato,
        "timestamp": ahora_mexico
    }

    # Insertar en la colección
    resultado = coleccion.insert_one(registro)
    registro["_id"] = str(resultado.inserted_id)

    return {
        "id": registro["_id"],
        "mensaje": "Asistencia registrada exitosamente",
        "registro": registro
    }



def obtener_todas_asistencias() -> List[Dict]:
    """
    Obtiene todos los registros de la colección 'asistencia_general'
    """
    db = get_db()
    coleccion = db.asistencia_general
    registros = list(coleccion.find().sort("timestamp", -1))  # Más recientes primero
    
    # Convertir ObjectId a string y timestamp a ISO format
    for registro in registros:
        registro["_id"] = str(registro["_id"])
        if isinstance(registro.get("timestamp"), datetime):
            registro["timestamp"] = registro["timestamp"].isoformat()
    
    return registros

def obtener_asistencias_por_matricula(matricula: str) -> List[Dict]:
    """
    Obtiene todos los registros de asistencia de una matrícula específica
    """
    db = get_db()
    coleccion = db.asistencia_general
    registros = list(coleccion.find({"matricula": matricula}).sort("timestamp", -1))
    
    # Convertir ObjectId a string y timestamp a ISO format
    for registro in registros:
        registro["_id"] = str(registro["_id"])
        if isinstance(registro.get("timestamp"), datetime):
            registro["timestamp"] = registro["timestamp"].isoformat()
    
    return registros
