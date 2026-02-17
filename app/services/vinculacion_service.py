"""
Servicios de lógica de negocio para operaciones con registros de vinculación.

Este módulo contiene las funciones que interactúan con MongoDB para:
- Registrar nuevos usuarios en la colección vinculacion_registros
- Obtener todos los registros de vinculación
- Eliminar registros de vinculación por teléfono
- Manejo de zona horaria de México para fechas y horas
"""
from datetime import datetime
from app.database import get_db
from typing import List, Dict, Optional
import pytz

def obtener_hora_mexico():
    """
    Obtiene la fecha y hora actual en horario de México (UTC-6)
    """
    zona_mexico = pytz.timezone('America/Mexico_City')
    ahora_mexico = datetime.now(zona_mexico)
    return ahora_mexico

def registrar_vinculacion(nombre: str, telefono: int) -> dict:
    """
    Registra un nuevo usuario en la colección 'vinculacion_registros'.
    - Guarda: nombre, telefono, fecha (formato: "dd/mm/aaaa a las HH:MM")
    - Almacena en la colección 'vinculacion_registros'
    """
    db = get_db()
    coleccion = db.vinculacion_registros
    
    # Obtener fecha y hora en horario de México
    ahora_mexico = obtener_hora_mexico()
    fecha_formato = ahora_mexico.strftime("%d/%m/%Y a las %H:%M")
    
    # Crear el registro
    registro = {
        "nombre": nombre,
        "telefono": telefono,
        "fecha": fecha_formato,
        "timestamp": ahora_mexico
    }
    
    # Insertar en la colección
    resultado = coleccion.insert_one(registro)
    registro["_id"] = str(resultado.inserted_id)
    
    return {
        "id": registro["_id"],
        "mensaje": "Registro de vinculación creado exitosamente",
        "registro": registro
    }

def obtener_todos_registros_vinculacion() -> List[Dict]:
    """
    Obtiene todos los registros de la colección 'vinculacion_registros'
    """
    db = get_db()
    coleccion = db.vinculacion_registros
    registros = list(coleccion.find().sort("timestamp", -1))  # Más recientes primero
    
    # Convertir ObjectId a string y timestamp a ISO format
    for registro in registros:
        registro["_id"] = str(registro["_id"])
        if isinstance(registro.get("timestamp"), datetime):
            registro["timestamp"] = registro["timestamp"].isoformat()
    
    return registros

def eliminar_registro_vinculacion_por_telefono(telefono: int) -> dict:
    """
    Elimina un registro de vinculación por su número de teléfono.
    Retorna información sobre el registro eliminado.
    """
    db = get_db()
    coleccion = db.vinculacion_registros
    
    # Buscar el registro por teléfono
    registro = coleccion.find_one({"telefono": telefono})
    
    if not registro:
        raise ValueError(f"No se encontró ningún registro con el teléfono {telefono}")
    
    # Eliminar el registro
    resultado = coleccion.delete_one({"telefono": telefono})
    
    if resultado.deleted_count == 0:
        raise ValueError(f"No se pudo eliminar el registro con el teléfono {telefono}")
    
    # Convertir ObjectId a string y timestamp a ISO format
    registro["_id"] = str(registro["_id"])
    if isinstance(registro.get("timestamp"), datetime):
        registro["timestamp"] = registro["timestamp"].isoformat()
    
    return {
        "mensaje": "Registro eliminado exitosamente",
        "registro_eliminado": registro
    }
