---
name: run-project
description: Launch the ZoomArtists app (FastAPI backend + Angular frontend + Postgres/Redis). Use when asked to run, start, serve, or boot up the project, the app, the backend, or the frontend.
---

# Run ZoomArtists

Full stack: **Postgres+PostGIS + Redis** (Docker) → **FastAPI** backend → **Angular** frontend.

## Prerequisites check

Before launching, verify tooling. If something is missing, stop and tell the user:

- `docker --version` — Docker Desktop must be installed AND running (the daemon).
- `uv --version` — Python package manager (install with `pip install uv` if missing).
- `node --version` — Node 20+.

Service ports: backend `8000`, frontend `4200`, postgres `5432`, redis `6379`. If a port is busy, surface it rather than guessing.

## Launch sequence

Run these in order. Steps 3 and 4 are long-running servers — start each with `run_in_background: true`.

### 1. Start infrastructure (Postgres + Redis)

```bash
cd "d:/CodeProjects/Agentic/ZoomArtists" && docker compose up -d
```

Wait until both containers are healthy:

```bash
docker compose ps
```

Both `zoomartists_postgres` and `zoomartists_redis` should show `(healthy)`.

### 2. Ensure backend env + run migrations

The backend reads `backend/.env`. If it does not exist, copy it:

```bash
cd "d:/CodeProjects/Agentic/ZoomArtists/backend" && [ -f .env ] || cp ../.env.example .env
```

Apply database migrations (PostGIS extension + tables). **First run only** needs the extension enabled — see "First-time database setup" below.

```bash
cd "d:/CodeProjects/Agentic/ZoomArtists/backend" && uv run alembic upgrade head
```

If there are **no migration files yet** (`backend/alembic/versions/` is empty), generate the initial one first:

```bash
cd "d:/CodeProjects/Agentic/ZoomArtists/backend" && uv run alembic revision --autogenerate -m "initial schema" && uv run alembic upgrade head
```

### 3. Start backend (background)

```bash
cd "d:/CodeProjects/Agentic/ZoomArtists/backend" && uv run uvicorn app.main:app --reload --port 8000
```

Verify: `curl http://localhost:8000/health` returns `{"status":"ok"}`.
API docs live at http://localhost:8000/docs.

### 4. Start frontend (background)

```bash
cd "d:/CodeProjects/Agentic/ZoomArtists/frontend" && npm start
```

App serves at http://localhost:4200.

## First-time database setup

PostGIS needs its extension enabled once. The `postgis/postgis` Docker image enables it automatically on the default database, so a fresh `docker compose up` usually needs nothing extra. If migrations fail with `type "geometry" does not exist`, run:

```bash
docker exec zoomartists_postgres psql -U zoomartists -d zoomartists -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

Then re-run the migration.

## Shutdown

```bash
# Stop the background backend/frontend tasks, then:
cd "d:/CodeProjects/Agentic/ZoomArtists" && docker compose down
```

Add `-v` to `docker compose down` only if the user wants to wipe the database volume.

## Convenience scripts

This skill ships helper scripts in its directory:

- `dev-up.ps1` — runs steps 1–2 (infra + migrations) and prints next commands.
- `dev-down.ps1` — stops everything.

Prefer running the steps individually (above) so server logs stream back to you. Use the scripts only if the user explicitly wants a one-shot.

## Troubleshooting

- **`docker` not found / daemon not running** → Docker Desktop isn't started. Ask the user to launch it.
- **Backend `ModuleNotFoundError`** → run `uv sync` in `backend/`.
- **Frontend `Cannot find module`** → run `npm install` in `frontend/`.
- **`connection refused` to Postgres** → containers not healthy yet; re-check `docker compose ps`.
- **CORS errors in browser** → confirm `BACKEND_CORS_ORIGINS` in `backend/.env` includes `http://localhost:4200`.
