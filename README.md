# Gestor de tareas

Aplicación móvil para gestionar tareas, hecha con **React Native (Expo)** y un backend en **FastAPI + SQLAlchemy**. Permite listar, crear, completar y eliminar tareas, buscar por nombre y filtrar por estado.

## Características

- Listado de tareas con contadores (total, completadas, pendientes)
- Crear tareas con título, descripción y prioridad (alta / media / baja)
- Marcar tareas como completadas o pendientes
- Eliminar tareas
- Búsqueda por nombre y filtro por estado (todas / pendientes / completadas)
- Manejo de errores de red con reintento y botón para simular fallos de la API
- Se puede conectar a la API remota o a un backend local

## Tecnologías

**App móvil:** Expo, React Native, Expo Router, TypeScript, Jest

**Backend:** FastAPI, SQLAlchemy (async), SQLite (aiosqlite), Uvicorn

## Estructura del proyecto

```
hvillalba/
├── estudiantes/                 # App móvil (Expo)
│   ├── app/                     # Pantallas (Expo Router)
│   │   ├── index.tsx            # Pantalla principal de tareas
│   │   └── guia.tsx             # Pantalla de guía
│   ├── src/
│   │   ├── components/          # TaskCard, StatusTabs
│   │   ├── config/api.ts        # URL de la API (local o remota)
│   │   ├── services/            # taskService.ts (llamadas a la API)
│   │   ├── types/               # Tipos de TypeScript
│   │   └── utils/               # Filtros y validaciones
│   ├── __tests__/               # Tests con Jest
│   └── app.json
└── fastapi_sqlalchemy_demo/     # Backend
    ├── main.py                  # Endpoints
    ├── models.py                # Modelo de base de datos
    ├── schemas.py               # Esquemas de validación
    └── database.py              # Conexión a SQLite
```

## Requisitos

- Node.js 18 o superior y npm
- Python 3.10 o superior (solo si vas a usar el backend local)
- La app **Expo Go** en el celular, o un emulador de Android / iOS

## Puesta en marcha

### Opción A: usar la API remota (solo Expo)

La app puede conectarse a `https://api.montenegroariel.com.ar`, así que no necesitás levantar el backend.

1. En `estudiantes/src/config/api.ts` verificá que esté:

   ```ts
   const MODE: 'remote' | 'local' = 'remote';
   ```

2. Instalá dependencias y levantá la app:

   ```bash
   cd estudiantes
   npm install
   npx expo start -c
   ```

3. Escaneá el código QR con Expo Go.

> En este modo se trabaja con los datos del servidor remoto, no con una base local.

### Opción B: usar el backend local

**Terminal 1: backend**

```bash
cd fastapi_sqlalchemy_demo
python -m venv venv

# Windows
venv\Scripts\activate
# Mac / Linux
source venv/bin/activate

pip install fastapi "uvicorn[standard]" sqlalchemy aiosqlite
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Verificá que funcione abriendo `http://localhost:8000/docs`.

**Terminal 2: app**

En `estudiantes/src/config/api.ts` cambiá:

```ts
const MODE: 'remote' | 'local' = 'local';
```

Y levantá Expo:

```bash
cd estudiantes
npm install
npx expo start -c
```

La IP de tu PC se detecta automáticamente. Si no conecta, definí `MANUAL_LOCAL_URL` en `api.ts` (por ejemplo `'http://192.168.0.15:8000'`).

**Notas para el modo local:**

- El celular y la PC deben estar en la misma red WiFi.
- Si el firewall bloquea la conexión, permití el puerto 8000.
- En el emulador de Android se usa `10.0.2.2` automáticamente.

## API

Documentación interactiva en `/docs` (Swagger).

| Método | Ruta            | Descripción                          |
| ------ | --------------- | ------------------------------------ |
| GET    | `/tasks/`       | Listar tareas                        |
| POST   | `/tasks/`       | Crear una tarea                      |
| GET    | `/tasks/{id}`   | Obtener una tarea                    |
| PUT    | `/tasks/{id}`   | Reemplazar una tarea                 |
| PATCH  | `/tasks/{id}`   | Actualizar campos (ej. `completed`)  |
| DELETE | `/tasks/{id}`   | Eliminar una tarea                   |

**Ejemplo de tarea:**

```json
{
  "id": 1,
  "title": "Revisar documentación",
  "description": "Leer la guía del proyecto",
  "completed": false,
  "priority": "media"
}
```

## Compatibilidad con versiones antiguas del servidor

La app tolera servidores que todavía no tienen el campo `priority` ni el endpoint `PATCH`:

- Si falta `priority`, se usa `media` por defecto.
- Si `PATCH` no existe, al completar una tarea se hace `GET` + `PUT`.

## Tests

```bash
cd estudiantes
npm test
```

Otros comandos útiles:

```bash
npm run typecheck    # Verificación de tipos
npm run doctor       # Diagnóstico de Expo
```

## Generar un APK

Se usa EAS Build (compila en la nube, sin necesidad de Android Studio).

1. Dejá la app en modo remoto (`MODE = 'remote'`).
2. Instalá EAS CLI e iniciá sesión:

   ```bash
   npm install -g eas-cli
   eas login
   ```

3. Desde `estudiantes/`, generá la configuración:

   ```bash
   eas build:configure
   ```

4. En `eas.json`, asegurate de tener este perfil:

   ```json
   {
     "build": {
       "preview": {
         "distribution": "internal",
         "android": { "buildType": "apk" }
       }
     }
   }
   ```

5. Compilá:

   ```bash
   eas build -p android --profile preview
   ```

Al terminar, EAS entrega un enlace para descargar el `.apk`.

## Hoja de ruta

- Actualizar el backend remoto con `priority` y `PATCH`
- Selector de prioridad y descripción al crear tareas
- Variables de entorno (`EXPO_PUBLIC_API_URL`) en lugar de la constante `MODE`
- Mejor manejo de errores y estados de carga

## Autor

Héctor Villalba