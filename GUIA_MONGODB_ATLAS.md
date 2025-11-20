# 🔐 Guía: Configurar MongoDB Atlas para Asistencia EDEC

## 📋 Paso a Paso: Crear Usuario y Obtener Contraseña

### Paso 1: Crear Cuenta en MongoDB Atlas

1. Ve a https://www.mongodb.com/cloud/atlas
2. Haz clic en "Try Free" o "Sign Up"
3. Completa el registro

### Paso 2: Crear un Cluster

1. Una vez dentro del dashboard, haz clic en "Build a Database"
2. Elige el plan **FREE (M0)**
3. Selecciona un proveedor de nube (AWS, Google Cloud, Azure)
4. Elige una región cercana a ti
5. Nombra tu cluster (ej: "Cluster0")
6. Haz clic en "Create"

**Nota**: La creación del cluster puede tardar 3-5 minutos.

### Paso 3: Crear Usuario de Base de Datos

1. En el menú lateral izquierdo, ve a **"Security"** → **"Database Access"**
   - O directamente: https://cloud.mongodb.com/v2#/security/database/users

2. Haz clic en el botón **"+ ADD DATABASE USER"** (esquina superior derecha)

3. Configura el usuario:
   - **Authentication Method**: Selecciona "Password"
   - **Username**: Ingresa un nombre (ej: `asistencia_user`, `admin`, `edec_user`)
   - **Password**: 
     - Opción A: Haz clic en "Autogenerate Secure Password" (recomendado)
     - Opción B: Crea tu propia contraseña
   - **Database User Privileges**: Selecciona "Atlas admin" (para desarrollo) o "Read and write to any database"

4. **⚠️ IMPORTANTE**: Si usaste "Autogenerate Secure Password":
   - **COPIA LA CONTRASEÑA INMEDIATAMENTE**
   - Guárdala en un lugar seguro
   - **No podrás verla de nuevo** después de cerrar esta ventana

5. Haz clic en "Add User"

### Paso 4: Configurar Acceso de Red

1. En el menú lateral, ve a **"Security"** → **"Network Access"**
   - O directamente: https://cloud.mongodb.com/v2#/security/network/list

2. Haz clic en **"+ ADD IP ADDRESS"**

3. Para desarrollo/pruebas:
   - Haz clic en **"Allow Access from Anywhere"**
   - Esto agregará `0.0.0.0/0` (permite acceso desde cualquier IP)
   - ⚠️ **Solo para desarrollo**. En producción, agrega IPs específicas.

4. Haz clic en "Confirm"

### Paso 5: Obtener la URI de Conexión

1. En el menú lateral, ve a **"Database"** → **"Connect"**
   - O haz clic en "Connect" en la tarjeta de tu cluster

2. Selecciona **"Connect your application"**

3. Selecciona:
   - **Driver**: Python
   - **Version**: 3.6 or later

4. Copia la cadena de conexión que aparece. Se verá así:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### Paso 6: Construir la URI Completa

Reemplaza los placeholders en la URI:

1. Reemplaza `<username>` con el nombre de usuario que creaste
2. Reemplaza `<password>` con la contraseña que obtuviste
3. (Opcional) Agrega el nombre de la base de datos después de `.net/`:
   ```
   mongodb+srv://asistencia_user:TuPassword123@cluster0.xxxxx.mongodb.net/asistencia_edec?retryWrites=true&w=majority
   ```

**Ejemplo completo**:
```
mongodb+srv://asistencia_user:MiPassword123!@cluster0.abc123.mongodb.net/asistencia_edec?retryWrites=true&w=majority
```

### Paso 7: Usar la URI en Render.com

1. En Render.com, ve a tu servicio → "Environment"
2. Agrega la variable de entorno:
   - **Key**: `MONGODB_URI`
   - **Value**: La URI completa que construiste (con usuario y contraseña)

## 🔑 ¿Olvidaste tu Contraseña?

Si olvidaste la contraseña del usuario:

1. Ve a "Security" → "Database Access"
2. Encuentra tu usuario en la lista
3. Haz clic en los tres puntos (⋯) junto al usuario
4. Selecciona "Edit" o "Reset Password"
5. Crea una nueva contraseña
6. **Guárdala inmediatamente**
7. Actualiza la URI en Render.com con la nueva contraseña

## ✅ Verificar la Conexión

Para verificar que tu URI funciona:

1. Desde tu máquina local, actualiza tu `.env`:
   ```env
   MONGODB_URI=mongodb+srv://usuario:password@cluster0.xxxxx.mongodb.net/asistencia_edec?retryWrites=true&w=majority
   ```

2. Ejecuta el script de inicialización:
   ```bash
   python backend/scripts/init_database.py
   ```

3. Si no hay errores, la conexión es correcta ✅

## 🛡️ Seguridad

### Para Desarrollo:
- Puedes usar "Allow Access from Anywhere" (0.0.0.0/0)
- Usa una contraseña fuerte pero fácil de recordar

### Para Producción:
- Restringe el acceso de IP solo a las IPs de Render.com
- Usa contraseñas muy seguras
- Considera usar usuarios con permisos limitados (solo lectura/escritura en la BD específica)

## 📝 Resumen Rápido

1. **Crear usuario**: Security → Database Access → + ADD DATABASE USER
2. **Copiar contraseña**: Si usas "Autogenerate", cópiala inmediatamente
3. **Permitir IPs**: Security → Network Access → Allow Access from Anywhere
4. **Obtener URI**: Database → Connect → Connect your application
5. **Reemplazar**: `<username>` y `<password>` en la URI
6. **Usar en Render**: Agregar como variable de entorno `MONGODB_URI`

## ❓ Problemas Comunes

### "Authentication failed"
- Verifica que el usuario y contraseña sean correctos
- Asegúrate de que no haya espacios en la URI
- Verifica que la contraseña no tenga caracteres especiales que necesiten codificación URL

### "IP not whitelisted"
- Ve a Network Access y agrega tu IP o "Allow Access from Anywhere"

### "Connection timeout"
- Verifica que el cluster esté completamente creado (puede tardar unos minutos)
- Verifica que la URI sea correcta

