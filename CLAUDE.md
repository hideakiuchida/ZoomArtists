# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

**ZoomArtists** — a map-based platform for discovering artistic events near you (seeded around Lima, Peru). Async FastAPI backend (Clean Architecture, PostGIS geo-queries) + Angular 21 frontend (MapLibre GL). Postgres+PostGIS and Redis run in Docker. The full product spec lives in `specs/SPECS.md`.

## Running the project

A `run-project` skill automates the full launch sequence — prefer invoking it. Manual commands:

```bash
# 1. Infra (Postgres+PostGIS + Redis)
docker compose up -d            # from repo root; wait for both containers "(healthy)" via `docker compose ps`

# 2. Backend (from backend/) — needs backend/.env (copy from ../.env.example if absent)
uv run alembic upgrade head     # apply migrations
uv run python seed.py           # load sample data (wipes events/artists/venues + demo user first)
uv run uvicorn app.main:app --reload --port 8000

# 3. Frontend (from frontend/)
npm start                       # serves at http://localhost:4200
```

Ports: backend `8000`, frontend `4200`, postgres `5432`, redis `6379`. API docs/Swagger at http://localhost:8000/docs (root `/` redirects there). Seeded demo organizer: `demo@zoomartists.app` / `demo1234`.

If migrations fail with `type "geometry" does not exist`, enable PostGIS once:
`docker exec zoomartists_postgres psql -U zoomartists -d zoomartists -c "CREATE EXTENSION IF NOT EXISTS postgis;"`

## Common commands

Backend (run from `backend/`, all via `uv run`):

```bash
uv sync                                              # install deps (fixes ModuleNotFoundError)
uv run pytest                                        # all tests (asyncio_mode=auto, no decorator needed)
uv run pytest path/to/test_x.py::test_name           # single test
uv run ruff check .                                  # lint (rules: E, F, I — line-length 100)
uv run ruff format .                                 # format
uv run alembic revision --autogenerate -m "msg"      # new migration after model changes
```

Frontend (run from `frontend/`):

```bash
npm test            # Vitest (jsdom) via @angular/build:unit-test
npm run build       # production build
```

Note: `backend/main.py` is a stub — the real ASGI app is `app.main:app`. Python 3.13 required.

## Backend architecture (Clean Architecture)

The dependency rule is enforced strictly: source dependencies point **inward only**. The `clean-architecture` skill is installed and the codebase follows it deliberately — preserve these boundaries when editing.

Layers under `backend/app/`, innermost first:

- **`domain/`** — `entities.py` (plain dataclasses: `User`, `Artist`, `Venue`, `Event`, `Coordinates` + enums; business rules as methods like `User.can_manage_event`, `Event.is_visible`) and `errors.py` (`DomainError` subclasses that know nothing about HTTP). No framework imports here.
- **`application/`** — use cases as small classes with an `execute(...)` method (e.g. `CreateEvent`, `GetNearbyEvents` in `events.py`). They depend on **ports** (`ports.py` — ABCs for repositories and services, defined in terms of domain entities) and pass data via DTOs (`dto.py`). Use cases never import infrastructure or FastAPI.
- **`infrastructure/`** — outward adapters that *implement* the ports: `persistence/repositories.py` (SQLAlchemy async repos), `persistence/models/` (ORM tables), `persistence/mappers.py` (ORM ↔ domain entity translation), `security/` (`BcryptPasswordHasher`, `JwtTokenService`), `config.py` (pydantic-settings, reads `.env`).
- **`api/`** — the HTTP delivery mechanism. `routes/` (thin controllers — translate request → DTO, instantiate a use case with injected ports, map the result entity → response schema), `schemas/` (Pydantic request/response models with `from_entity`/`from_result` helpers), `deps.py` (FastAPI dependency wiring — the *only* place that knows both abstractions and concrete implementations; builds repos per-request, resolves current user, `require_role(...)`), `errors.py` (translates `DomainError` → HTTP status).
- **`main.py`** — composition root: assembles FastAPI, mounts routers under `/api`, registers the domain-error handler, owns the engine lifecycle and CORS/rate-limiting.

**Request flow:** `routes/*` → builds a DTO/command → `application/*` use case (depends on `ports`) → `infrastructure/persistence/repositories` (the port implementation) → `mappers` convert ORM rows to domain entities → use case returns entity → route maps entity to a `schemas/*` response.

**When adding a feature, touch the layers in inward-to-outward order:** domain entity/rule → port method (if new persistence needed) → use case → repository implementation + mapper → route + schema → wire in `deps.py`.

Key patterns:
- **Errors:** raise `DomainError` subclasses (`NotFoundError`, `PermissionDeniedError`, `ConflictError`, `ValidationError`, `AuthenticationError`) from domain/application code. `api/errors.py` maps each to a status code centrally — do not raise `HTTPException` in use cases.
- **Geo:** PostGIS via GeoAlchemy2. Coordinates are WGS84 (SRID 4326), stored as `POINT(lng lat)`. "Nearby" queries live in `SqlAlchemyEventRepository.find_nearby`. The Postgres image is `postgis/postgis:16-3.4`.
- **Auth:** JWT bearer (`python-jose`), bcrypt hashing. Access + refresh tokens. Roles: `attendee`, `artist`, `organizer`, `admin`; gate endpoints with `require_role(...)`.
- **DB sessions:** one `AsyncSession` per request via `get_db`; `expire_on_commit=False`. `engine.echo` is on in development.

## Frontend architecture (Angular 21)

Standalone components, lazy-loaded routes, signals-based services. Under `frontend/src/app/`:

- **`core/`** — `models/` (TS interfaces mirroring backend schemas), `services/` (`AuthService`, `EventService`, `GeolocationService` — call the API), `interceptors/auth.interceptor.ts` (attaches `Authorization: Bearer` from `AuthService.getAccessToken()`).
- **`features/`** — `map/` (MapLibre GL map, the default route `''`), `events/` (event-panel + event-popup), `auth/` (route `auth`), `search/`. Routes are lazy `loadComponent` (`app.routes.ts`).
- Providers wired in `app.config.ts`. API base URL in `src/environments/environment.ts` (`http://localhost:8000/api`).

Styling: Tailwind CSS v4 (via `@tailwindcss/postcss` + Vite) and SCSS component styles. Prettier: 100 col, single quotes.

## Conventions

- Backend follows the dependency rule above — never import outward (domain must not import application/infrastructure/api; application must not import infrastructure/api).
- DTOs/commands carry data across the application boundary; never pass ORM models or Pydantic schemas into use cases.
- After changing ORM models in `infrastructure/persistence/models/`, generate a migration with `alembic revision --autogenerate` and review it before committing.
- `backend/` is its own git repository (the workspace root is not a git repo).
