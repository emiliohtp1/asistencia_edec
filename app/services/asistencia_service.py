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
    Registra asistencia por día: un documento por día por usuario.
    
    - Si tipo_registro = "entrada": crea o actualiza la hora de entrada.
    - Si tipo_registro = "salida": actualiza el documento existente del día.
    """
    db = get_db()

    # Obtener datos del usuario
    usuario = obtener_usuario_por_matricula(matricula)
    if not usuario.encontrado:
        raise ValueError(f"Usuario con matrícula {matricula} no encontrado")

    # Obtener colección semanal
    nombre_coleccion = obtener_nombre_coleccion_semanal()
    coleccion = db[nombre_coleccion]

    # Fecha actual en formato YYYY-MM-DD
    ahora = datetime.now()
    fecha_hoy = ahora.strftime("%Y-%m-%d")
    hora_actual = ahora.strftime("%H:%M")

    # Buscar si ya existe un registro para ese usuario hoy
    registro_existente = coleccion.find_one({
        "matricula": matricula,
        "fecha": fecha_hoy
    })

    # ----------------------------
    # 1️⃣ Registrar ENTRADA
    # ----------------------------
    if tipo_registro == "entrada":
        if registro_existente:
            # Si ya tiene entrada, podemos actualizarla o no permitir duplicado
            return {
                "mensaje": "La entrada ya había sido registrada",
                "registro": registro_existente
            }

        # Crear el registro del día
        nuevo_registro = {
            "matricula": matricula,
            "nombre": usuario.nombre_completo,
            "carrera": usuario.carrera,
            "fecha": fecha_hoy,
            "entrada": hora_actual,
            "salida": None
        }

        resultado = coleccion.insert_one(nuevo_registro)

        verificar_y_generar_excel_semanal(nombre_coleccion)

        return {
            "mensaje": "Entrada registrada",
            "id": str(resultado.inserted_id),
            "registro": nuevo_registro
        }

    # ----------------------------
    # 2️⃣ Registrar SALIDA
    # ----------------------------
    elif tipo_registro == "salida":
        if not registro_existente:
            raise ValueError("No existe una entrada registrada para hoy")

        if registro_existente.get("salida"):
            return {
                "mensaje": "La salida ya había sido registrada",
                "registro": registro_existente
            }

        # Actualizar salida
        coleccion.update_one(
            {"_id": registro_existente["_id"]},
            {"$set": {"salida": hora_actual}}
        )

        registro_existente["salida"] = hora_actual

        return {
            "mensaje": "Salida registrada",
            "registro": registro_existente
        }

    else:
        raise ValueError("tipo_registro debe ser 'entrada' o 'salida'")


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

def obtener_todos_usuarios_db() -> List[Dict]: # 💡 Cambié el nombre para evitar confusión
    """
    Obtiene y formatea todos los usuarios de la colección 'login'
    """
    db = get_db()
    coleccion = db.login
    # 1. Obtener los registros
    registros = list(coleccion.find().sort("timestamp", -1))
    
    # ⚠️ ERROR CORREGIDO: El 'return registros' estaba prematuramente. Lo eliminamos.
    
    # 2. Procesar y formatear los registros
    for registro in registros:
        # Convertir ObjectId a string
        registro["_id"] = str(registro["_id"]) 
        
        # Convertir datetime a formato ISO (string) si existe
        if isinstance(registro.get("timestamp"), datetime):
            registro["timestamp"] = registro["timestamp"].isoformat()
    
    # 3. Devolver la lista ya procesada
    return registros