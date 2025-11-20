# 🔐 Variables de Entorno para Render.com

## Variables que debes configurar en Render.com

Cuando despliegues en Render.com, ve a tu servicio → **"Environment"** → **"Add Environment Variable"** y agrega las siguientes variables:

### ✅ Variables Requeridas

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `MONGODB_URI` | `mongodb+srv://emiliohtp_db_user:PUyvTLcwWKOQ4wwM@cluster0.cvdcchr.mongodb.net/asistencia_edec?retryWrites=true&w=majority` | URI completa de conexión a MongoDB Atlas |
| `DATABASE_NAME` | `asistencia_edec` | Nombre de la base de datos |
| `EXCEL_DIR` | `./excel_reports` | Carpeta donde se guardarán los archivos Excel |

### ⚠️ Variables que NO debes configurar

Render.com las proporciona automáticamente:
- `PORT` - Render lo asigna automáticamente
- `HOST` - No es necesario, Render lo maneja

## 📋 Copiar y Pegar Rápido

Copia estas variables directamente en Render.com:

```
MONGODB_URI=mongodb+srv://emiliohtp_db_user:PUyvTLcwWKOQ4wwM@cluster0.cvdcchr.mongodb.net/asistencia_edec?retryWrites=true&w=majority
DATABASE_NAME=asistencia_edec
EXCEL_DIR=./excel_reports
```

## 🔒 Seguridad

- ✅ El archivo `.env` está en `.gitignore`, no se subirá a GitHub
- ✅ Las variables sensibles (como la contraseña de MongoDB) solo están en Render.com
- ✅ Nunca subas el archivo `.env` a GitHub

## 📝 Pasos en Render.com

1. Ve a tu servicio en Render.com
2. Haz clic en **"Environment"** en el menú lateral
3. Haz clic en **"Add Environment Variable"**
4. Agrega cada variable una por una:
   - Key: `MONGODB_URI`
   - Value: `mongodb+srv://emiliohtp_db_user:PUyvTLcwWKOQ4wwM@cluster0.cvdcchr.mongodb.net/asistencia_edec?retryWrites=true&w=majority`
   - Haz clic en "Save"
5. Repite para `DATABASE_NAME` y `EXCEL_DIR`
6. Reinicia el servicio si ya estaba desplegado

## ✅ Verificación

Después de configurar las variables, verifica que el servicio se inicie correctamente:
- Ve a "Logs" en Render.com
- Deberías ver: `✅ Conectado a MongoDB`
- Si hay errores, verifica que la URI sea correcta y que las IPs estén permitidas en MongoDB Atlas

