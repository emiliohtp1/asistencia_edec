# 📡 Endpoints de la API - Sistema de Asistencia EDEC

## 🔗 Base URL
```
http://localhost:8000  (desarrollo)
https://tu-api.onrender.com  (producción)
```

## 📚 Documentación Interactiva
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 👥 Endpoints de Usuarios

### 1. Obtener Usuario por Matrícula
```http
GET /api/usuarios/{matricula}
```

**Ejemplo:**
```bash
GET /api/usuarios/A001
```

**Respuesta:**
```json
{
  "matricula": "A001",
  "nombre_completo": "Juan Pérez García",
  "carrera": "Ingeniería en Sistemas",
  "tipo": "alumno",
  "encontrado": true
}
```

---

### 2. Obtener Todos los Alumnos
```http
GET /api/usuarios/alumnos/todos
```

**Ejemplo:**
```bash
GET /api/usuarios/alumnos/todos
```

**Respuesta:**
```json
{
  "total": 3,
  "alumnos": [
    {
      "_id": "...",
      "matricula": "A001",
      "nombre_completo": "Juan Pérez García",
      "carrera": "Ingeniería en Sistemas"
    },
    {
      "_id": "...",
      "matricula": "A002",
      "nombre_completo": "María González",
      "carrera": "Ingeniería Industrial"
    }
  ]
}
```

---

### 3. Obtener Todos los Maestros
```http
GET /api/usuarios/maestros/todos
```

**Ejemplo:**
```bash
GET /api/usuarios/maestros/todos
```

**Respuesta:**
```json
{
  "total": 2,
  "maestros": [
    {
      "_id": "...",
      "matricula": "M001",
      "nombre_completo": "Dr. Roberto Sánchez",
      "carrera": "Ingeniería en Sistemas"
    },
    {
      "_id": "...",
      "matricula": "M002",
      "nombre_completo": "Dra. Ana Martínez",
      "carrera": "Ingeniería Industrial"
    }
  ]
}
```

---

## 📋 Endpoints de Asistencias

### 1. Registrar Asistencia (Colecciones Semanales)
```http
POST /api/asistencias/registrar
```

**Body:**
```json
{
  "matricula": "A001",
  "tipo_registro": "entrada"
}
```

**Nota:** Este endpoint:
- Busca el usuario por matrícula
- Crea el registro en la colección semanal (ej: `asistencias_2024_Semana01`)
- Genera archivos Excel automáticamente

**Respuesta:**
```json
{
  "id": "...",
  "mensaje": "Asistencia del usuario registrada",
  "registro": {
    "matricula": "A001",
    "nombre_completo": "Juan Pérez García",
    "tipo_registro": "entrada",
    "fecha": "2024-01-15",
    "hora": "08:30:00",
    "timestamp": "2024-01-15T08:30:00",
    "carrera": "Ingeniería en Sistemas",
    "tipo_usuario": "alumno"
  }
}
```

---

### 2. Obtener Asistencias de la Semana Actual
```http
GET /api/asistencias/semana-actual
```

**Ejemplo:**
```bash
GET /api/asistencias/semana-actual
```

**Respuesta:**
```json
{
  "coleccion": "asistencias_2024_Semana01",
  "total": 10,
  "asistencias": [...]
}
```

---

### 3. Obtener Todas las Asistencias (Colección "asistencia")
```http
GET /api/asistencias/todas
```

**Ejemplo:**
```bash
GET /api/asistencias/todas
```

**Respuesta:**
```json
{
  "coleccion": "asistencia",
  "total": 50,
  "asistencias": [
    {
      "_id": "...",
      "matricula": "A001",
      "nombre_completo": "Juan Pérez García",
      "tipo_registro": "entrada",
      "fecha": "2024-01-15",
      "hora": "08:30:00",
      "timestamp": "2024-01-15T08:30:00",
      "carrera": "Ingeniería en Sistemas",
      "tipo_usuario": "alumno"
    }
  ]
}
```

---

### 4. Crear Asistencia Directa (Colección "asistencia")
```http
POST /api/asistencias/crear
```

**Body:**
```json
{
  "matricula": "A001",
  "nombre_completo": "Juan Pérez García",
  "tipo_registro": "entrada",
  "fecha": "2024-01-15",
  "hora": "08:30:00",
  "carrera": "Ingeniería en Sistemas",
  "tipo_usuario": "alumno"
}
```

**Campos opcionales:**
- `fecha`: Si no se proporciona, se usa la fecha actual
- `hora`: Si no se proporciona, se usa la hora actual
- `carrera`: Opcional
- `tipo_usuario`: Opcional

**Ejemplo mínimo:**
```json
{
  "matricula": "A001",
  "nombre_completo": "Juan Pérez García",
  "tipo_registro": "entrada"
}
```

**Respuesta:**
```json
{
  "id": "...",
  "mensaje": "Asistencia creada exitosamente en la colección 'asistencia'",
  "registro": {
    "_id": "...",
    "matricula": "A001",
    "nombre_completo": "Juan Pérez García",
    "tipo_registro": "entrada",
    "fecha": "2024-01-15",
    "hora": "08:30:00",
    "timestamp": "2024-01-15T08:30:00",
    "carrera": "Ingeniería en Sistemas",
    "tipo_usuario": "alumno"
  }
}
```

---

## 🔍 Resumen de Endpoints

| Método | Endpoint | Descripción | Colección |
|--------|----------|-------------|-----------|
| GET | `/api/usuarios/{matricula}` | Obtener usuario por matrícula | alumnos/maestros |
| GET | `/api/usuarios/alumnos/todos` | Obtener todos los alumnos | alumnos |
| GET | `/api/usuarios/maestros/todos` | Obtener todos los maestros | maestros |
| POST | `/api/asistencias/registrar` | Registrar asistencia (semanal) | asistencias_YYYY_SemanaXX |
| GET | `/api/asistencias/semana-actual` | Asistencias semana actual | asistencias_YYYY_SemanaXX |
| GET | `/api/asistencias/todas` | Todas las asistencias | asistencia |
| POST | `/api/asistencias/crear` | Crear asistencia directa | asistencia |

---

## 🧪 Ejemplos con cURL

### Obtener todos los alumnos
```bash
curl http://localhost:8000/api/usuarios/alumnos/todos
```

### Obtener todos los maestros
```bash
curl http://localhost:8000/api/usuarios/maestros/todos
```

### Obtener todas las asistencias
```bash
curl http://localhost:8000/api/asistencias/todas
```

### Crear asistencia directa
```bash
curl -X POST http://localhost:8000/api/asistencias/crear \
  -H "Content-Type: application/json" \
  -d '{
    "matricula": "A001",
    "nombre_completo": "Juan Pérez García",
    "tipo_registro": "entrada",
    "carrera": "Ingeniería en Sistemas",
    "tipo_usuario": "alumno"
  }'
```

---

## ⚠️ Notas Importantes

1. **Colecciones Semanales vs Colección "asistencia"**:
   - `/api/asistencias/registrar` → Guarda en colecciones semanales (ej: `asistencias_2024_Semana01`)
   - `/api/asistencias/crear` → Guarda directamente en la colección `asistencia`

2. **Validación de tipo_registro**:
   - Solo acepta: `"entrada"` o `"salida"`
   - Cualquier otro valor retornará error 400

3. **Ordenamiento**:
   - Alumnos/Maestros: Ordenados por matrícula (ascendente)
   - Asistencias: Ordenadas por timestamp (más recientes primero)

4. **Formato de Fecha/Hora**:
   - Fecha: `YYYY-MM-DD` (ej: `2024-01-15`)
   - Hora: `HH:MM:SS` (ej: `08:30:00`)

