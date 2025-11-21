from datetime import datetime, timedelta
from app.database import get_db
from app.models.asistencia import Asistencia
from app.services.usuario_service import obtener_usuario_por_matricula
import os
import pandas as pd
from app.config import Config
from typing import List, Dict

def obtener_nombre_coleccion_semanal():
    """
    Obtiene el nombre de la colección semanal basado en la fecha actual.
    Formato: asistencias_YYYY_SemanaXX
    """
    hoy = datetime.now()
    # Obtener el primer día de la semana (lunes)
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    año = inicio_semana.year
    # Calcular el número de semana del año
    semana = inicio_semana.isocalendar()[1]
    return f"asistencias_{año}_Semana{semana:02d}"

def registrar_asistencia(matricula: str, tipo_registro: str) -> dict:
    """
    Registra una asistencia en la colección semanal correspondiente
    """
    db = get_db()
    
    # Obtener datos del usuario
    usuario = obtener_usuario_por_matricula(matricula)
    if not usuario.encontrado:
        raise ValueError(f"Usuario con matrícula {matricula} no encontrado")
    
    # Obtener nombre de la colección semanal
    nombre_coleccion = obtener_nombre_coleccion_semanal()
    
    # Crear el registro de asistencia
    ahora = datetime.now()
    registro = {
        "matricula": matricula,
        "nombre_completo": usuario.nombre_completo,
        "tipo_registro": tipo_registro,
        "fecha": ahora.strftime("%Y-%m-%d"),
        "hora": ahora.strftime("%H:%M:%S"),
        "timestamp": ahora,
        "carrera": usuario.carrera,
        "tipo_usuario": usuario.tipo
    }
    
    # Insertar en la colección semanal
    coleccion = db[nombre_coleccion]
    resultado = coleccion.insert_one(registro)
    
    # Verificar si es el primer registro de la semana y generar Excel si es necesario
    verificar_y_generar_excel_semanal(nombre_coleccion)
    
    return {
        "id": str(resultado.inserted_id),
        "mensaje": f"Asistencia del usuario registrada",
        "registro": registro
    }

def verificar_y_generar_excel_semanal(nombre_coleccion: str):
    """
    Verifica si ya existe un archivo Excel para esta semana.
    Si no existe o hay nuevos registros, genera/actualiza el archivo Excel.
    """
    db = get_db()
    coleccion = db[nombre_coleccion]
    
    # Obtener todos los registros de la semana
    registros = list(coleccion.find().sort("timestamp", 1))
    
    if not registros:
        return
    
    # Crear directorio si no existe
    os.makedirs(Config.EXCEL_DIR, exist_ok=True)
    
    # Nombre del archivo Excel
    nombre_archivo = f"{nombre_coleccion}.xlsx"
    ruta_archivo = os.path.join(Config.EXCEL_DIR, nombre_archivo)
    
    # Preparar datos para Excel
    datos_excel = []
    for registro in registros:
        datos_excel.append({
            "Matrícula": registro["matricula"],
            "Nombre Completo": registro["nombre_completo"],
            "Tipo Usuario": registro.get("tipo_usuario", ""),
            "Carrera": registro.get("carrera", ""),
            "Tipo Registro": registro["tipo_registro"],
            "Fecha": registro["fecha"],
            "Hora": registro["hora"],
            "Timestamp": registro["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Crear DataFrame y guardar en Excel
    df = pd.DataFrame(datos_excel)
    df.to_excel(ruta_archivo, index=False, engine='openpyxl')
    
    print(f"✅ Archivo Excel generado: {ruta_archivo}")

def obtener_asistencias_semana(nombre_coleccion: str = None):
    """
    Obtiene todas las asistencias de la semana actual
    """
    db = get_db()
    if nombre_coleccion is None:
        nombre_coleccion = obtener_nombre_coleccion_semanal()
    
    coleccion = db[nombre_coleccion]
    registros = list(coleccion.find().sort("timestamp", 1))
    
    # Convertir ObjectId a string
    for registro in registros:
        registro["_id"] = str(registro["_id"])
        if isinstance(registro.get("timestamp"), datetime):
            registro["timestamp"] = registro["timestamp"].isoformat()
    
    return registros

def obtener_todas_asistencias() -> List[Dict]:
    """
    Obtiene todos los registros de la colección 'asistencia'
    """
    db = get_db()
    coleccion = db.asistencia
    registros = list(coleccion.find().sort("timestamp", -1))  # Más recientes primero
    
    # Convertir ObjectId a string y timestamp a ISO format
    for registro in registros:
        registro["_id"] = str(registro["_id"])
        if isinstance(registro.get("timestamp"), datetime):
            registro["timestamp"] = registro["timestamp"].isoformat()
    
    return registros

def crear_asistencia_directa(datos: dict) -> dict:
    """
    Crea un registro de asistencia directamente en la colección 'asistencia'
    """
    db = get_db()
    coleccion = db.asistencia
    
    # Preparar el registro
    ahora = datetime.now()
    registro = {
        "matricula": datos["matricula"],
        "nombre_completo": datos["nombre_completo"],
        "tipo_registro": datos["tipo_registro"],
        "fecha": datos.get("fecha") or ahora.strftime("%Y-%m-%d"),
        "hora": datos.get("hora") or ahora.strftime("%H:%M:%S"),
        "timestamp": ahora,
        "carrera": datos.get("carrera", ""),
        "tipo_usuario": datos.get("tipo_usuario", "")
    }
    
    # Insertar en la colección
    resultado = coleccion.insert_one(registro)
    
    # Convertir ObjectId a string para la respuesta
    registro["_id"] = str(resultado.inserted_id)
    registro["timestamp"] = registro["timestamp"].isoformat()
    
    return {
        "id": str(resultado.inserted_id),
        "mensaje": "Asistencia creada exitosamente en la colección 'asistencia'",
        "registro": registro
    }

def obtener_todos_usuarios_login() -> List[Dict]:
    """
    Obtiene todos los usuarios de la colección 'login'
    """
    db = get_db()
    coleccion = db.login
    registros = list(coleccion.find().sort("timestamp", -1))
    return registros
    for registro in registros:
        registro["_id"] = str(registro["_id"])
        if isinstance(registro.get("timestamp"), datetime):
            registro["timestamp"] = registro["timestamp"].isoformat()
    
    return registros
