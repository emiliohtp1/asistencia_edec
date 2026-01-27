"""
Servicios de lógica de negocio para operaciones con asistencias.

Este módulo contiene las funciones que interactúan con MongoDB para:
- Registrar asistencias con matrícula, nombre, fecha y hora
- Obtener listas completas de asistencias
- Consultar asistencias por matrícula específica
- Manejo de zona horaria de México para fechas y horas
"""
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

def registrar_asistencia(matricula: str, nombre: str) -> dict:
    """
    Registra la asistencia de entrada de una matrícula.
    - Solo permite un registro por matrícula por día
    - Guarda: Matricula, Nombre, Fecha (DD/MM/YYYY), Hora (HH:MM)
    - Almacena en la colección 'asistencia_general_apodaca'
    """

    db = get_db()
    coleccion = db.asistencia_general_apodaca

    # Obtener fecha y hora en horario de México
    ahora_mexico = obtener_hora_mexico()
    fecha_formato = ahora_mexico.strftime("%d/%m/%Y")
    hora_formato = ahora_mexico.strftime("%H:%M")

    # Verificar si ya existe un registro para esta matrícula hoy
    registro_existente = coleccion.find_one({
        "Matricula": matricula,
        "Fecha": fecha_formato
    })

    if registro_existente:
        raise ValueError(f"La matrícula {matricula} ya tiene un registro de asistencia para hoy ({fecha_formato})")

    # Crear el registro con campos en mayúscula (como en MongoDB)
    registro = {
        "Matricula": matricula,
        "Nombre": nombre,
        "Fecha": fecha_formato,
        "Hora": hora_formato,
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

def obtener_todas_asistencias_apodaca() -> List[Dict]:
    """
    Obtiene todos los registros de asistencia de la colección 'asistencia_general_apodaca'
    """
    db = get_db()
    coleccion = db.asistencia_general_apodaca
    registros = list(coleccion.find().sort("timestamp", -1))  # Más recientes primero
    
    # Convertir ObjectId a string y timestamp a ISO format
    for registro in registros:
        registro["_id"] = str(registro["_id"])
        if isinstance(registro.get("timestamp"), datetime):
            registro["timestamp"] = registro["timestamp"].isoformat()
    
    return registros

def obtener_asistencias_apodaca_por_matricula(matricula: str) -> List[Dict]:
    """
    Obtiene todos los registros de asistencia de una matrícula específica
    de la colección 'asistencia_general_apodaca'
    """
    db = get_db()
    coleccion = db.asistencia_general_apodaca
    # Buscar por Matricula (con mayúscula) como string
    registros = list(coleccion.find({"Matricula": matricula}).sort("timestamp", -1))
    
    # Si no se encuentra, intentar como int
    if not registros:
        try:
            matricula_int = int(matricula)
            registros = list(coleccion.find({"Matricula": matricula_int}).sort("timestamp", -1))
        except (ValueError, TypeError):
            pass
    
    # Convertir ObjectId a string y timestamp a ISO format
    for registro in registros:
        registro["_id"] = str(registro["_id"])
        if isinstance(registro.get("timestamp"), datetime):
            registro["timestamp"] = registro["timestamp"].isoformat()
    
    return registros

# ============================================================================
# FUNCIONES PARA FICHADOS DE APODACA (Base de datos asistencia_edec)
# ============================================================================

def registrar_fichado_apodaca(fichado_data: dict) -> Dict:
    """
    Registra un fichado en la base de datos asistencia_edec, colección fichados_apodaca.
    Agrega automáticamente la fecha_registro_ficha con fecha y hora actual.
    """
    db = get_db()
    coleccion = db.fichados_apodaca
    
    # Obtener fecha y hora actual en horario de México
    ahora_mexico = obtener_hora_mexico()
    
    # Crear el documento del fichado
    fichado = {
        "matricula": fichado_data["matricula"],
        "nombre": fichado_data["nombre"],
        "coordinador": fichado_data["coordinador"],
        "graduado": fichado_data["graduado"],
        "correo": fichado_data["correo"],
        "campus": fichado_data["campus"],
        "programa": fichado_data["programa"],
        "ciclo": fichado_data["ciclo"],
        "turno": fichado_data["turno"],
        "fecha_registro_ficha": ahora_mexico
    }
    
    # Insertar en la base de datos
    resultado = coleccion.insert_one(fichado)
    fichado["_id"] = str(resultado.inserted_id)
    
    # Convertir fecha_registro_ficha a ISO format
    if isinstance(fichado.get("fecha_registro_ficha"), datetime):
        fichado["fecha_registro_ficha"] = fichado["fecha_registro_ficha"].isoformat()
    
    return fichado

def obtener_fichados_apodaca_agrupados() -> List[Dict]:
    """
    Obtiene todos los fichados de la colección fichados_apodaca.
    Si existen varios objetos con el mismo nombre y matricula, muestra solo uno
    con un campo cantidad_fichas que indica cuántas veces se repite.
    """
    db = get_db()
    coleccion = db.fichados_apodaca
    
    # Obtener todos los fichados
    fichados = list(coleccion.find().sort("fecha_registro_ficha", -1))
    
    # Agrupar por nombre y matricula
    fichados_agrupados = {}
    
    for fichado in fichados:
        clave = f"{fichado.get('nombre', '')}_{fichado.get('matricula', '')}"
        
        if clave not in fichados_agrupados:
            # Primera vez que vemos esta combinación, guardar el fichado
            fichado_agrupado = {
                "matricula": fichado.get("matricula", ""),
                "nombre": fichado.get("nombre", ""),
                "coordinador": fichado.get("coordinador", ""),
                "graduado": fichado.get("graduado", ""),
                "correo": fichado.get("correo", ""),
                "campus": fichado.get("campus", ""),
                "programa": fichado.get("programa", ""),
                "ciclo": fichado.get("ciclo", ""),
                "turno": fichado.get("turno", ""),
                "cantidad_fichas": 1
            }
            fichados_agrupados[clave] = fichado_agrupado
        else:
            # Ya existe, incrementar contador
            fichados_agrupados[clave]["cantidad_fichas"] += 1
    
    # Convertir el diccionario a lista
    resultado = list(fichados_agrupados.values())
    
    return resultado