"""Composition root.

The outermost entry point: it assembles the framework (FastAPI), mounts the
interface-adapter routers, registers the domain-error translator, and owns the
database engine lifecycle. Everything it depends on points inward.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.errors import add_exception_handlers
from app.api.routes import artists, auth, events, venues
from app.infrastructure.config import settings
from app.infrastructure.persistence import models  # noqa: F401 — registers tables on Base
from app.infrastructure.persistence.database import engine

API_DESCRIPTION = """
**ZoomArtists** — discover artistic events near you.

A Clean Architecture FastAPI backend: HTTP controllers translate requests into
application use cases, which operate on pure domain entities through repository
ports implemented by the infrastructure layer.

### Authentication
Most write endpoints require a **Bearer access token**.

1. Call `POST /api/auth/register` or `POST /api/auth/login` to obtain an
   `access_token`.
2. Click the **Authorize 🔒** button (top right) and paste the token.
3. Authorized requests will send the `Authorization: Bearer <token>` header.

Seeded demo organizer — `demo@zoomartists.app` / `demo1234`.
"""

# Per-tag descriptions surfaced as section headers in Swagger UI.
TAGS_METADATA = [
    {"name": "auth", "description": "Registration, login, token refresh, and the current user."},
    {"name": "events", "description": "Browse nearby events and manage their lifecycle."},
    {"name": "artists", "description": "Artist profiles and following."},
    {"name": "venues", "description": "Venue directory with geolocation."},
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup — could run Alembic here in dev
    yield
    # On shutdown
    await engine.dispose()


limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="ZoomArtists API",
    description=API_DESCRIPTION,
    version="0.1.0",
    lifespan=lifespan,
    openapi_tags=TAGS_METADATA,
    contact={"name": "ZoomArtists", "email": "dev@zoomartists.app"},
    license_info={"name": "Proprietary"},
    servers=[{"url": "http://localhost:8000", "description": "Local development"}],
    swagger_ui_parameters={
        "persistAuthorization": True,  # keep the token across page reloads
        "displayRequestDuration": True,
        "docExpansion": "none",
        "filter": True,
    },
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
add_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(events.router, prefix="/api")
app.include_router(artists.router, prefix="/api")
app.include_router(venues.router, prefix="/api")


@app.get("/", include_in_schema=False)
async def root():
    # Land visitors on the interactive Swagger docs.
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
