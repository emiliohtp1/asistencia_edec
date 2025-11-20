"""
Script para inicializar la base de datos con datos de ejemplo
Ejecutar: python scripts/init_database.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import connect_db, get_db

def init_database():
    """Inicializa la base de datos con datos de ejemplo"""
    connect_db()
    db = get_db()
    
    # Datos de ejemplo para alumnos
    alumnos_ejemplo = [
        {
            "matricula": "A001",
            "nombre_completo": "Juan Pérez García",
            "carrera": "Ingeniería en Sistemas"
        },
        {
            "matricula": "A002",
            "nombre_completo": "María González López",
            "carrera": "Ingeniería Industrial"
        },
        {
            "matricula": "A003",
            "nombre_completo": "Carlos Rodríguez Martínez",
            "carrera": "Administración"
        }
    ]
    
    # Datos de ejemplo para maestros
    maestros_ejemplo = [
        {
            "matricula": "M001",
            "nombre_completo": "Dr. Roberto Sánchez",
            "carrera": "Ingeniería en Sistemas"
        },
        {
            "matricula": "M002",
            "nombre_completo": "Dra. Ana Martínez",
            "carrera": "Ingeniería Industrial"
        }
    ]
    
    # Limpiar colecciones existentes (opcional, comentar si no se desea)
    # db.alumnos.delete_many({})
    # db.maestros.delete_many({})
    
    # Insertar alumnos
    for alumno in alumnos_ejemplo:
        if not db.alumnos.find_one({"matricula": alumno["matricula"]}):
            db.alumnos.insert_one(alumno)
            print(f"✅ Alumno insertado: {alumno['matricula']} - {alumno['nombre_completo']}")
        else:
            print(f"⚠️  Alumno ya existe: {alumno['matricula']}")
    
    # Insertar maestros
    for maestro in maestros_ejemplo:
        if not db.maestros.find_one({"matricula": maestro["matricula"]}):
            db.maestros.insert_one(maestro)
            print(f"✅ Maestro insertado: {maestro['matricula']} - {maestro['nombre_completo']}")
        else:
            print(f"⚠️  Maestro ya existe: {maestro['matricula']}")
    
    print("\n✅ Base de datos inicializada correctamente")

if __name__ == "__main__":
    init_database()

