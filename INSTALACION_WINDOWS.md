# Guía de Instalación para Windows

## Problema con pandas en Python 3.13

Si encuentras errores al instalar pandas, necesitas instalar las herramientas de compilación de Visual Studio.

### Solución Rápida: Instalar Visual Studio Build Tools

1. Descarga Visual Studio Build Tools desde: https://visualstudio.microsoft.com/downloads/
2. Selecciona "Herramientas de compilación para Visual Studio"
3. Durante la instalación, asegúrate de seleccionar:
   - "Desarrollo para el escritorio con C++"
   - "SDK de Windows 10/11"

### Alternativa: Usar Python 3.11 o 3.12

Si prefieres evitar la instalación de herramientas de compilación:

1. Descarga Python 3.11 o 3.12 desde python.org
2. Crea un nuevo entorno virtual con esa versión
3. Instala las dependencias normalmente

### Verificar la instalación

Después de instalar Visual Studio Build Tools, intenta nuevamente:

```bash
pip install -r requirements.txt
```

