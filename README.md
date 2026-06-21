# ZoomArtists

> *"El arte está más cerca de lo que crees."*

Plataforma web basada en un **mapa interactivo** para descubrir eventos artísticos cercanos —conciertos, exposiciones, teatro, danza, cine independiente, performances y más— con información detallada del evento y los artistas en una interfaz dinámica tipo Spotify. Sembrada inicialmente alrededor de Lima, Perú.

La especificación de producto completa vive en [`specs/SPECS.md`](specs/SPECS.md).

## Stack

| Capa | Tecnología |
|---|---|
| **Frontend** | Angular 21 (standalone components, signals, lazy routes) · MapLibre GL · Tailwind CSS v4 · SCSS |
| **Backend** | FastAPI async · Clean Architecture · SQLAlchemy 2.0 (async) + GeoAlchemy2 · Pydantic v2 · Alembic |
| **Datos** | PostgreSQL + PostGIS (consultas geoespaciales) · Redis (caché) |
| **Auth** | JWT (access + refresh) con `python-jose` · hashing bcrypt · roles (attendee/artist/organizer/admin) |
| **Infra dev** | Docker Compose (Postgres + Redis) · `uv` (Python) · Python 3.13 |

## Estructura del repositorio

```
ZoomArtists/
├── backend/            # API FastAPI (Clean Architecture)
│   └── app/
│       ├── domain/         # Entidades puras + errores de dominio (sin frameworks)
│       ├── application/    # Casos de uso, ports (interfaces) y DTOs
│       ├── infrastructure/ # Repos SQLAlchemy, mappers, security, config
│       ├── api/            # Routes, schemas Pydantic, deps, errores HTTP
│       └── main.py         # Composition root (arma la app, monta /api)
├── frontend/           # SPA Angular 21
│   └── src/app/
│       ├── core/           # models, services, interceptors, guards
│       ├── features/       # map, events, artists, auth, search
│       └── shared/
├── specs/SPECS.md      # Especificación de producto v1.1
├── docker-compose.yml  # Postgres+PostGIS + Redis
└── CLAUDE.md           # Guía para agentes / convenciones del repo
```

> El backend sigue estrictamente la **Dependency Rule**: las dependencias del código fuente apuntan **solo hacia adentro** (domain ← application ← infrastructure/api). Las reglas de negocio no conocen FastAPI, SQLAlchemy ni HTTP.

## Puesta en marcha

**Requisitos:** Docker, Python 3.13 + [`uv`](https://github.com/astral-sh/uv), Node.js (Angular 21).

### 1. Infraestructura (Postgres+PostGIS + Redis)

```bash
docker compose up -d            # desde la raíz del repo
docker compose ps               # esperar a que ambos contenedores estén "(healthy)"
```

### 2. Backend (desde `backend/`)

Necesita un archivo `backend/.env` (copiar de [`.env.example`](.env.example) si no existe).

```bash
uv sync                                 # instalar dependencias
uv run alembic upgrade head             # aplicar migraciones
uv run python seed.py                   # cargar datos de ejemplo
uv run uvicorn app.main:app --reload --port 8000
```

Si las migraciones fallan con `type "geometry" does not exist`, habilitar PostGIS una vez:

```bash
docker exec zoomartists_postgres psql -U zoomartists -d zoomartists -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

### 3. Frontend (desde `frontend/`)

```bash
npm install
npm start                               # sirve en http://localhost:4200
```

### Puertos y accesos

| Servicio | URL / Puerto |
|---|---|
| Frontend | http://localhost:4200 |
| Backend (API) | http://localhost:8000 |
| Swagger / OpenAPI | http://localhost:8000/docs (`/` redirige aquí) |
| Postgres | `5432` |
| Redis | `6379` |

**Organizador demo sembrado:** `demo@zoomartists.app` / `demo1234`

## Comandos comunes

**Backend** (desde `backend/`, vía `uv run`):

```bash
uv run pytest                                       # tests (asyncio_mode=auto)
uv run pytest path/to/test_x.py::test_name          # un solo test
uv run ruff check .                                 # lint (E, F, I — línea 100)
uv run ruff format .                                # format
uv run alembic revision --autogenerate -m "msg"     # migración tras cambiar modelos
```

**Frontend** (desde `frontend/`):

```bash
npm test            # Vitest (jsdom)
npm run build       # build de producción
```

## API — endpoints principales

Base: `/api`. Documentación interactiva en `/docs`.

| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/api/auth/register` · `/login` · `/refresh` | Registro y emisión de tokens |
| `GET` | `/api/events` | Listar eventos con filtros |
| `GET` | `/api/events/nearby` | Eventos dentro de un radio geoespacial (PostGIS) |
| `GET` | `/api/events/{id}` | Detalle de evento |
| `POST` `PATCH` `DELETE` | `/api/events/{id}` | Gestionar eventos (rol organizer) |
| `GET` | `/api/artists/{id}` | Perfil de artista |
| `POST` `DELETE` | `/api/artists/{id}/follow` | Seguir / dejar de seguir |
| `GET` | `/api/venues/{id}` | Detalle de venue |

Ejemplo de consulta geoespacial:

```
GET /api/events/nearby?lat=-12.0464&lng=-77.0428&radius=5000&category=music&isFree=false&limit=50
```

> Las coordenadas son WGS84 (SRID 4326), almacenadas como `POINT(lng lat)` con índice GiST. El radio se expresa en metros.

## Documentación

- [`specs/SPECS.md`](specs/SPECS.md) — especificación de producto completa (visión, UX, modelos de datos, roadmap).
- [`CLAUDE.md`](CLAUDE.md) — arquitectura detallada y convenciones para contribuir.
