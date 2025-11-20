# 🚀 Guía de Despliegue en Render.com

Esta guía te ayudará a desplegar el backend de Asistencia EDEC en Render.com.

## 📋 Requisitos Previos

1. **Cuenta en Render.com** (gratis): https://render.com
2. **Cuenta en MongoDB Atlas** (gratis): https://www.mongodb.com/cloud/atlas
   - O usar MongoDB local si tienes un servidor dedicado

## 🔧 Paso 1: Configurar MongoDB Atlas

1. Ve a https://www.mongodb.com/cloud/atlas y crea una cuenta gratuita
2. Crea un nuevo cluster (elige la opción gratuita M0)
3. Crea un usuario de base de datos:
   - Ve a "Database Access" → "Add New Database User"
   - Crea un usuario y contraseña (guárdalos)
4. Configura el acceso de red:
   - Ve a "Network Access" → "Add IP Address"
   - Selecciona "Allow Access from Anywhere" (0.0.0.0/0) para desarrollo
   - O agrega la IP específica de Render en producción
5. Obtén la cadena de conexión:
   - Ve a "Database" → "Connect" → "Connect your application"
   - Copia la cadena de conexión (URI)
   - Reemplaza `<password>` con tu contraseña y `<dbname>` con `asistencia_edec`
   - Ejemplo: `mongodb+srv://usuario:password@cluster0.xxxxx.mongodb.net/asistencia_edec?retryWrites=true&w=majority`

## 📤 Paso 2: Subir el Código a GitHub

1. Crea un repositorio en GitHub
2. Sube tu código (asegúrate de que `.env` esté en `.gitignore`)
3. Anota la URL del repositorio

## 🌐 Paso 3: Desplegar en Render.com

### Opción A: Usando render.yaml (Recomendado)

1. Ve a https://dashboard.render.com
2. Haz clic en "New +" → "Blueprint"
3. Conecta tu repositorio de GitHub
4. Render detectará automáticamente el archivo `render.yaml`
5. Revisa la configuración y haz clic en "Apply"

### Opción B: Configuración Manual

1. Ve a https://dashboard.render.com
2. Haz clic en "New +" → "Web Service"
3. Conecta tu repositorio de GitHub
4. Configura el servicio:
   - **Name**: `asistencia-edec-api` (o el que prefieras)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend` (importante: especifica la carpeta backend)

5. Configura las Variables de Entorno:
   - Haz clic en "Environment" en el menú lateral
   - Agrega las siguientes variables:
     ```
     MONGODB_URI=mongodb+srv://usuario:password@cluster0.xxxxx.mongodb.net/asistencia_edec?retryWrites=true&w=majority
     DATABASE_NAME=asistencia_edec
     EXCEL_DIR=./excel_reports
     ```
     **Nota**: Render proporciona `PORT` automáticamente, no necesitas configurarlo.

6. Haz clic en "Create Web Service"

## ⚙️ Paso 4: Configurar Variables de Entorno en Render

En el dashboard de Render, ve a tu servicio → "Environment" y agrega:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `MONGODB_URI` | `mongodb+srv://...` | URI de conexión de MongoDB Atlas |
| `DATABASE_NAME` | `asistencia_edec` | Nombre de la base de datos |
| `EXCEL_DIR` | `./excel_reports` | Carpeta para archivos Excel |

**Importante**: 
- No configures `PORT` ni `HOST`, Render los maneja automáticamente
- Asegúrate de que la URI de MongoDB incluya la contraseña correcta

## 🗄️ Paso 5: Inicializar la Base de Datos

Una vez desplegado, puedes inicializar la base de datos de dos formas:

### Opción 1: Desde tu máquina local

1. Actualiza tu `.env` local con la URI de MongoDB Atlas
2. Ejecuta:
   ```bash
   python backend/scripts/init_database.py
   ```

### Opción 2: Usando el Shell de Render

1. En Render, ve a tu servicio → "Shell"
2. Ejecuta:
   ```bash
   python scripts/init_database.py
   ```

## 🔗 Paso 6: Obtener la URL de tu API

Una vez desplegado, Render te proporcionará una URL como:
```
https://asistencia-edec-api.onrender.com
```

**Nota**: En el plan gratuito, el servicio puede tardar unos segundos en iniciar si ha estado inactivo.

## 📝 Paso 7: Actualizar el Frontend

Actualiza `frontend/js/config.js` con la URL de tu API en Render:

```javascript
const API_CONFIG = {
    BASE_URL: 'https://tu-api.onrender.com',  // Cambia esto
    ENDPOINTS: {
        USUARIO: '/api/usuarios',
        ASISTENCIA: '/api/asistencias'
    }
};
```

## ✅ Verificación

1. Visita `https://tu-api.onrender.com` - Deberías ver el mensaje de bienvenida
2. Visita `https://tu-api.onrender.com/docs` - Deberías ver la documentación de Swagger
3. Prueba el endpoint: `https://tu-api.onrender.com/api/usuarios/A001`

## 🐛 Solución de Problemas

### Error de conexión a MongoDB
- Verifica que la URI de MongoDB sea correcta
- Asegúrate de que la IP de Render esté permitida en MongoDB Atlas
- Verifica que el usuario y contraseña sean correctos

### Error al iniciar el servicio
- Revisa los logs en Render → "Logs"
- Verifica que el "Start Command" sea correcto
- Asegúrate de que el "Root Directory" esté configurado como `backend`

### El servicio se duerme (plan gratuito)
- En el plan gratuito, Render "duerme" el servicio después de 15 minutos de inactividad
- La primera petición después de dormir puede tardar 30-60 segundos
- Considera usar un servicio de "ping" para mantenerlo activo

## 📊 Archivos Excel en Render

**Importante**: Los archivos Excel se generan en el sistema de archivos de Render, que es **efímero**. 
Si necesitas persistir los archivos Excel, considera:
- Usar un servicio de almacenamiento (S3, Google Cloud Storage, etc.)
- Guardar los archivos en MongoDB como binarios
- Usar un servicio de almacenamiento de Render (si está disponible)

## 🔒 Seguridad en Producción

1. **CORS**: Actualiza `allow_origins` en `backend/app/main.py` para especificar solo tu dominio:
   ```python
   allow_origins=["https://tu-dominio.com"]
   ```

2. **MongoDB**: Restringe el acceso de IP en MongoDB Atlas solo a las IPs de Render

3. **Variables de Entorno**: Nunca subas el archivo `.env` a GitHub

## 📚 Recursos Adicionales

- Documentación de Render: https://render.com/docs
- Documentación de MongoDB Atlas: https://docs.atlas.mongodb.com
- Documentación de FastAPI: https://fastapi.tiangolo.com

## 💡 Notas Importantes

- El plan gratuito de Render tiene limitaciones (sueño después de inactividad)
- MongoDB Atlas gratuito tiene límites de almacenamiento (512 MB)
- Los archivos Excel en Render son temporales (se pierden al reiniciar)
- Considera usar un servicio de almacenamiento para archivos Excel en producción

