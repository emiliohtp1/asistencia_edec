from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import connect_db, close_db
from app.routes import usuarios, asistencias
from app.config import Config

app = FastAPI(
    title="Sistema de Asistencia EDEC",
    description="API para registro de asistencia de alumnos y maestros",
    version="1.0.0"
)

# Configurar CORS para permitir peticiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar el dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(usuarios.router)
app.include_router(asistencias.router)

@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicación"""
    connect_db()
    # Crear directorio de Excel si no existe
    import os
    os.makedirs(Config.EXCEL_DIR, exist_ok=True)

@app.on_event("shutdown")
async def shutdown_event():
    """Evento que se ejecuta al cerrar la aplicación"""
    close_db()

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "mensaje": "API de Sistema de Asistencia EDEC",
        "version": "1.0.0",
        "endpoints": {
            "usuarios": "/api/usuarios/{matricula}",
            "asistencias": "/api/asistencias/registrar",
            "asistencias_semana": "/api/asistencias/semana-actual"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)

