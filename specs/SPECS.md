# ZoomArtists — Especificaciones de Producto v1.2

> **Leyenda de estado:** ✅ implementado · 🚧 pendiente / parcial.
> Las secciones sin marca describen decisiones de producto ya reflejadas en el código.
> Datos de ejemplo sembrados alrededor de **Lima, Perú** (`seed.py`), precios en PEN.

---

## 1. Visión General

**ZoomArtists** es una plataforma web que conecta audiencias con eventos artísticos locales mediante un mapa interactivo geolocalizado. Los usuarios descubren conciertos, exposiciones, obras de teatro, performances y más eventos culturales en su radio de proximidad, con información detallada del evento y los artistas desplegada en una interfaz dinámica tipo Spotify.

**Tagline:** *"El arte está más cerca de lo que crees."*

---

## 2. Usuarios Objetivo

| Segmento | Descripción |
|---|---|
| **Asistentes** | Personas que buscan eventos culturales cercanos para asistir |
| **Artistas** | Músicos, pintores, actores, performers que quieren visibilidad |
| **Organizadores** | Promotores, galerías, teatros, clubes que publican eventos |
| **Turistas** | Visitantes que buscan vida cultural local |

---

## 3. Categorías de Eventos

- Música en vivo (conciertos, jam sessions, recitales)
- Exposiciones de arte (galerías, museos, arte urbano)
- Teatro y danza
- Spoken word y poesía
- Cine independiente y proyecciones
- Performances callejeros
- Festivales culturales
- Talleres y clases artísticas

---

## 4. Funcionalidades Core

### 4.1 Mapa Interactivo (Vista Principal)

- Mapa de pantalla completa renderizado con **MapLibre GL JS** (estilo oscuro de OpenFreeMap)
- Detección automática de geolocalización del usuario (con permiso)
- Selector de radio de distancia: 1 km / 5 km / 10 km / 25 km
- **Círculo de radio auto-ajustado:** el círculo translúcido de búsqueda permanece siempre
  centrado en el **área visible** del mapa y el zoom se recalcula para que quepa por completo,
  ocupando ~90% de la dimensión visible más pequeña. Se re-ajusta al iniciar, al cambiar el
  radio y al redimensionar la ventana (con *debounce*). El área visible se calcula descontando
  la UI flotante (cabecera, filtros, controles) y el panel derecho de 380px en modo web, de modo
  que el círculo nunca queda tapado por el panel. En mobile el panel es un *bottom sheet* y no
  descuenta ancho.
- Marcadores con íconos visuales diferenciados por categoría de evento
- Animaciones suaves al desplazarse y hacer zoom
- Controles: zoom, centrar en ubicación actual
- Filtros flotantes sobre el mapa: por categoría (centrados respecto al área visible, no al
  viewport completo, para no descentrarse por el panel derecho en web)

### 4.2 Popup del Evento (al hacer click en marcador)

Popup compacto que aparece sobre el marcador con:

```
┌─────────────────────────────────┐
│  [imagen/thumbnail del evento]  │
│  🎵 CONCIERTO                   │
│  Nombre del Evento              │
│  📍 Venue Name · 2.3 km         │
│  📅 Sáb 20 Jun · 21:00          │
│  💰 $150 MXN / Gratis           │
│  ─────────────────────────────  │
│  [Ver detalles →]  [♥ Guardar] │
└─────────────────────────────────┘
```

- Click en "Ver detalles" abre el panel lateral derecho
- Hover sobre el popup resalta el marcador con animación
- El popup incluye avatar pequeño del artista principal

### 4.3 Panel Lateral Derecho — "Detalle del Evento" (Estilo Spotify)

Panel a la derecha (ancho: 380px en desktop, 100% en mobile).

**Comportamiento responsivo:**
- **Web (> 640px):** el panel está **siempre visible**. Cuando el usuario aún no ha
  seleccionado ningún evento, muestra un **resumen tipo lista de "eventos top"** — los eventos
  cercanos ordenados por distancia (miniatura, badge de categoría, título, venue, distancia,
  fecha y precio). Al hacer click en una tarjeta se abre el detalle del evento; el botón `[←]`
  regresa a la lista.
- **Mobile (≤ 640px):** el panel es un *bottom sheet* que **solo aparece al seleccionar** un
  evento (desde un marcador). La lista de eventos top se oculta para no tapar el mapa.
- Estados internos del panel: `cargando` (skeleton mientras se resuelve el detalle) →
  `detalle` (evento seleccionado) → `lista` (sin selección).

**Secciones del panel (vista de detalle):**

#### Header del Evento
- Imagen de portada a todo el ancho del panel con gradiente inferior
- Badge de categoría (ej: 🎭 TEATRO)
- Nombre del evento en tipografía grande
- Venue con link a Google Maps
- Fecha, hora y duración estimada
- Precio / "Entrada libre"
- Botones: `[Obtener Entradas]` `[♥]` `[↗ Compartir]`

#### Artistas
- Cards horizontales con foto del artista, nombre, género/disciplina ✅
- Click en card de artista expande mini-perfil con: 🚧
  - Bio corta (2-3 líneas)
  - Tags de género/estilo
  - Links a redes sociales (Instagram, Spotify, SoundCloud, YouTube)
  - Botón `[Seguir Artista]`

#### Contenido Multimedia
- Galería de imágenes del evento (scroll horizontal, `loading="lazy"`) ✅
- Video embed (YouTube/Vimeo) vía `video_url` del evento ✅
- Reproductor de audio embebido (preview de tracks si aplica) 🚧
- Reproducción automática de preview al abrir el panel (con ícono de mute visible) 🚧

#### Detalles del Venue
- Dirección completa ✅
- Información de accesibilidad ✅
- Transporte cercano (metro, bus) ✅
- Link a Google Maps ✅
- Mapa en miniatura del venue dentro del panel 🚧
- Capacidad y aforo 🚧

#### Más Eventos en este Venue 🚧
- Scroll horizontal de cards de próximos eventos en el mismo lugar

#### Footer del Panel
- `[← Cerrar]` en esquina superior izquierda del panel
- Fondo del panel: oscuro semitransparente con efecto blur (glassmorphism)

### 4.4 Barra de Búsqueda Global

- Barra flotante centrada en la parte superior del mapa ✅
- Autocompletado con debounce RxJS y resultados en tiempo real ✅ (UI)
- Al seleccionar resultado: el mapa vuela (fly-to) hacia la ubicación ✅
- Búsqueda por: nombre de evento, artista, venue, género, ciudad

> ⚠️ El componente consulta `GET /api/events?q=…&limit=8`, endpoint **aún no implementado** en
> el backend (ver §8). Hasta que exista, el autocompletado no devuelve resultados.

### 4.5 Publicación de Eventos (para organizadores)

Área de organizador protegida por rol (`organizerGuard`), con dos rutas:

- `/organizer` — **dashboard**: lista de los eventos propios (`GET /api/events/mine`) con
  acciones de editar y eliminar.
- `/organizer/events/new` y `/organizer/events/:id/edit` — **formulario** de creación/edición.

**Formulario actual** — página única con secciones agrupadas (no stepper): ✅

1. **Detalles:** título, categoría (selector visual por color), descripción
2. **Fecha y lugar:** inicio, fin (opcional) y selección de venue — elegir uno existente
   (`GET /api/venues`) o crear uno nuevo inline (nombre, dirección, ciudad, país, lat/lng)
3. **Entradas:** entrada libre / precio + moneda, link de venta, aforo
4. **Multimedia:** URLs de imagen de portada, galería y video (por enlace, sin upload)

**Pendiente** 🚧: stepper por pasos, upload de archivos a S3/R2, selección de venue con pin
sobre el mapa, asociación de artistas desde el formulario, recurrencia y vista previa del
popup/panel antes de publicar.

### 4.6 Perfiles de Artista 🚧

*Aún no implementado en el frontend.* El backend ya expone `GET /api/artists/{id}` y los
endpoints de follow/unfollow; el panel lateral muestra las cards de artista del evento pero el
mini-perfil expandido y la página dedicada están pendientes.

- Página de perfil dedicada accesible desde el panel lateral
- Portfolio multimedia: tracks, videos, galería
- Historial de eventos pasados y próximos
- Botón de "Seguir" para notificaciones de nuevos eventos
- Links a redes sociales y plataformas de streaming

### 4.7 Sistema de Usuarios

| Rol | `UserRole` | Capacidades |
|---|---|---|
| **Visitante** | *(sin sesión)* | Ver mapa, popup, panel de detalles, buscar |
| **Usuario registrado** | `attendee` | + Guardar eventos, seguir artistas, recibir notificaciones |
| **Artista** | `artist` | + Crear perfil artístico, asociarse a eventos |
| **Organizador** | `organizer` | + Publicar y administrar sus eventos (`/organizer`) |
| **Admin** | `admin` | + Administrar cualquier evento, moderar y aprobar publicaciones |

El alta pública (`POST /api/auth/register`) solo admite `attendee` u `organizer` — los roles
`artist` y `admin` se asignan internamente — y la pantalla de registro ofrece ese selector.
Las reglas viven en el dominio
(`User.can_manage_event`, `User.has_any_role`) y se aplican en el borde HTTP con
`require_role(...)`; `GET /api/events/mine` está abierto a `organizer`, `admin` y `artist`.

---

## 5. Diseño UI/UX

### 5.1 Principios de Diseño

- **Inmersivo:** El mapa ocupa el 100% del viewport; la UI flota sobre él
- **Oscuro por defecto:** Tema oscuro con acentos en colores vibrantes según categoría
- **Fluidez:** Transiciones suaves (300-500ms) en todas las interacciones
- **Mobile-first:** Diseño responsivo con gestos touch nativos

### 5.2 Paleta de Colores por Categoría

Fuente de verdad: `CATEGORY_COLORS` / `CATEGORY_ICONS` / `CATEGORY_LABELS` en
`frontend/src/app/core/models/event.model.ts`.

| Categoría (`EventCategory`) | Etiqueta | Color de acento |
|---|---|---|
| `music` | Música | `#7c3aed` — Violeta |
| `visual_art` | Arte Visual | `#f59e0b` — Ámbar |
| `theater` | Teatro | `#ec4899` — Rosa |
| `dance` | Danza | `#f97316` — Naranja |
| `spoken_word` | Spoken Word | `#10b981` — Esmeralda |
| `cinema` | Cine | `#3b82f6` — Azul |
| `festival` | Festival | `#ef4444` — Rojo |
| `workshop` | Taller | `#06b6d4` — Cian |
| `street_performance` | Performance Callejero | `#84cc16` — Lima |

### 5.3 Layout General

```
┌──────────────────────────────────────────┬────────────┐
│    [Logo] [🔍 Buscar...] [👤]  ← centrado │  PANEL     │
│                                    en área │  DERECHO   │
│      [All][🎵][🎨][🎭][🎬] ← filtros      │            │
│                                  centrados │ ┌────────┐ │
│              M A P A                       │ │ Evento │ │
│   (área visible = viewport − panel)        │ │ top 1  │ │
│          ╭───────────╮                     │ ├────────┤ │
│          │  ◜ radio ◝ │  📍📍               │ │ Evento │ │
│          │  ◟ círculo◞│    📍              │ │ top 2  │ │
│          ╰───────────╯                     │ ├────────┤ │
│                                            │ │  ...   │ │
│  [1km 5km 10km 25km]      [🎯]             │ └────────┘ │
└──────────────────────────────────────────┴────────────┘
   El círculo se centra en el área visible (sin el panel) y
   el zoom se ajusta para que quepa entero. La cabecera y los
   filtros se centran respecto a esa misma área, no al viewport.
   En web, sin selección el panel muestra la lista de eventos top.
```

### 5.4 Estados y Micro-interacciones

- **Marcador hover:** Escala a 1.2x con sombra de color de categoría + nombre del evento en tooltip
- **Marcador activo:** Pulso (ping animation) en el color de la categoría
- **Panel lateral:** en web permanece fijo a la derecha (lista de eventos top ⇄ detalle); en
  mobile entra como *bottom sheet* al seleccionar un evento. Glassmorphism con backdrop blur.
- **Carga de eventos:** Skeleton screens mientras cargan los datos
- **Radio de distancia:** Círculo translúcido centrado en el área visible; el zoom se auto-ajusta
  para que el círculo entero quepa en pantalla (responsivo al tamaño de ventana y al radio elegido)
- **UI flotante centrada:** cabecera y filtros de categoría se centran respecto al área visible
  (viewport menos el panel de 380px en web) mediante la variable CSS `--panel-w`
- **Fly-to:** Animación de vuelo suave al centrar en un evento desde búsqueda

---

## 6. Arquitectura Técnica

### 6.1 Stack Tecnológico Recomendado

**Frontend — Angular**
- **Framework:** Angular 21 con Standalone Components y Signals (sin NgModules)
- **Mapa:** `maplibre-gl` v5 usado directamente (sin wrapper); estilo oscuro de OpenFreeMap.
  No se usa Mapbox ni `ngx-mapbox-gl` — MapLibre es open source y no requiere API key
- **Estilos:** Tailwind CSS v4 (vía `@tailwindcss/postcss` + Vite) + SCSS por componente.
  Sin Angular Material: los overlays, popups y el panel son componentes propios
- **Animaciones:** transiciones CSS custom (`@angular/animations` disponible, poco usado)
- **Estado:** Angular Signals + `computed()`/`effect()` en servicios `providedIn: 'root'`.
  NgRx Signal Store queda como opción futura si el estado se vuelve complejo
- **HTTP:** `HttpClient` con `authInterceptor` funcional (adjunta el Bearer token)
- **Formularios:** Reactive Forms con validadores custom
- **Routing:** Angular Router con lazy `loadComponent` + guards por rol
- **Tests:** Vitest (jsdom) vía `@angular/build:unit-test`
- **Audio:** Howler.js en un `AudioPlayerService` 🚧 (pendiente, ver §4.3)

**Backend — Python**
- **Framework:** **FastAPI** — async, alto rendimiento, auto-genera OpenAPI docs (Swagger UI en `/docs`, ReDoc en `/redoc`)
- **Arquitectura:** **Clean Architecture** (ver 6.2) — reglas de negocio independientes del framework
- **ORM:** SQLAlchemy 2.0 (async) + **GeoAlchemy2** para queries PostGIS
- **Migraciones:** Alembic
- **Validación:** Pydantic v2 (integrado en FastAPI)
- **Base de Datos:** PostgreSQL 16 + **PostGIS** 3.4 (imagen `postgis/postgis:16-3.4`)
- **Server:** Uvicorn (dev, `--reload`); + Gunicorn en producción
- **Gestión de deps:** `uv` (Python 3.13)
- **Cache:** Redis — contenedor levantado y `REDIS_URL` configurada, pero el caché por
  geohash aún **no está implementado** 🚧
- **Storage:** AWS S3 o Cloudflare R2 con `boto3` (imágenes, audio) 🚧
- **Tareas en background:** Celery + Redis Broker (notificaciones push) 🚧
- **CDN:** Cloudflare 🚧

**Autenticación**
- Backend: `python-jose` para JWT access/refresh tokens + `bcrypt` para hashing de contraseñas ✅
- Frontend: `authInterceptor` + `organizerGuard` (guard de ruta por rol) ✅
- Providers OAuth: Google, Apple (via `authlib`) 🚧

**Infraestructura**
- Frontend: Netlify o Firebase Hosting (Angular SPA estática)
- Backend: Railway o Fly.io (contenedor Docker con FastAPI)
- CI/CD: GitHub Actions — lint + test + build + deploy
- Docker Compose para desarrollo local (app + postgres + redis)

### 6.2 Clean Architecture del Backend

El backend está estructurado en **círculos concéntricos** siguiendo la *Dependency Rule*: las dependencias del código fuente siempre apuntan **hacia adentro**, hacia las políticas de más alto nivel. Las reglas de negocio no saben nada de FastAPI, SQLAlchemy ni HTTP — estos son *detalles* enchufables en el círculo más externo.

```
        ┌───────────────────────────────────────────────┐
        │  Infrastructure / API  (frameworks & drivers)  │
        │  FastAPI · SQLAlchemy · PostGIS · bcrypt · JWT  │
        │   ┌───────────────────────────────────────┐    │
        │   │   Application  (casos de uso + ports)  │    │
        │   │    ┌─────────────────────────────┐     │    │
        │   │    │   Domain  (entidades puras)  │     │    │
        │   │    │   Event · Artist · Venue ·   │     │    │
        │   │    │   User · Coordinates · errors│     │    │
        │   │    └─────────────────────────────┘     │    │
        │   └───────────────────────────────────────┘    │
        └───────────────────────────────────────────────┘
              ▲ las dependencias apuntan hacia adentro ▲
```

| Capa | Responsabilidad | No puede importar |
|---|---|---|
| **Domain** | Entidades de negocio puras (dataclasses), value objects y errores de dominio. Reglas que existirían sin software (`User.can_manage_event`, `Event.is_visible`). | Nada de frameworks (ni FastAPI, ni SQLAlchemy, ni Pydantic). |
| **Application** | Casos de uso (interactors: `CreateEvent`, `RegisterUser`, `FollowArtist`…), DTOs de comando/resultado y **ports** (interfaces de repositorios y servicios). | `infrastructure`, `api`, frameworks. Solo depende de `domain`. |
| **Infrastructure** | Implementaciones concretas de los ports: repositorios SQLAlchemy + mappers ORM↔entidad, `BcryptPasswordHasher`, `JwtTokenService`, config. | — (círculo externo). |
| **API (Interface Adapters)** | Controllers HTTP delgados, schemas Pydantic con *presenters* (`from_entity`), wiring de inyección de dependencias y traducción de errores de dominio → códigos HTTP. | — (círculo externo). |

**Mecanismos clave:**

- **Dependency Inversion:** los casos de uso dependen de *ports* abstractos (`EventRepository`, `PasswordHasher`, `TokenService`) definidos en `application`; las implementaciones concretas viven en `infrastructure` y se inyectan desde afuera. La base de datos, el hashing y el formato de token son intercambiables sin tocar la lógica de negocio.
- **Entidades ≠ filas de BD:** las entidades de dominio son dataclasses puras; los modelos SQLAlchemy son un detalle de persistencia. Un módulo de `mappers` traduce entre ambos, evitando que los tipos del ORM se filtren hacia adentro.
- **Errores de dominio:** la lógica lanza `NotFoundError`, `ConflictError`, `AuthenticationError`, `PermissionDeniedError` (sin conocer HTTP). `api/errors.py` los traduce a `404/400/401/403` en un único lugar.
- **Composition root:** `app/main.py` ensambla el framework, monta los routers, registra el traductor de errores y administra el ciclo de vida del engine.

### 6.3 Estructura de carpetas del backend

```
backend/app/
├── domain/                      # Círculo interno — reglas de negocio puras
│   ├── entities.py              #   Event, Artist, Venue, User, Coordinates + enums
│   └── errors.py                #   DomainError jerarquía (NotFound, Conflict, …)
├── application/                 # Casos de uso (application business rules)
│   ├── ports.py                 #   Interfaces: repositorios + PasswordHasher/TokenService
│   ├── dto.py                   #   Comandos y resultados (RegisterCommand, NearbyQuery…)
│   ├── auth.py                  #   RegisterUser, LoginUser, RefreshTokens, AuthenticateToken
│   ├── events.py                #   GetNearbyEvents, CreateEvent, UpdateEvent, SaveEvent…
│   ├── artists.py               #   GetArtist, CreateArtist, FollowArtist, UnfollowArtist
│   └── venues.py                #   GetVenue, CreateVenue
├── infrastructure/              # Detalles: frameworks & drivers
│   ├── config.py                #   Settings (pydantic-settings)
│   ├── persistence/
│   │   ├── database.py          #   engine async, sessionmaker, Base, get_db
│   │   ├── models/              #   Modelos SQLAlchemy + GeoAlchemy2 (PostGIS)
│   │   ├── mappers.py           #   ORM ↔ entidades de dominio
│   │   └── repositories.py      #   SqlAlchemy{User,Artist,Venue,Event}Repository
│   └── security/
│       ├── password_hasher.py   #   BcryptPasswordHasher (implementa el port)
│       └── token_service.py     #   JwtTokenService (implementa el port)
├── api/                         # Interface adapters (delivery HTTP)
│   ├── deps.py                  #   Inyección de dependencias (repos, servicios, current_user)
│   ├── errors.py                #   DomainError → respuesta HTTP
│   ├── schemas/                 #   DTOs Pydantic con presenters (from_entity)
│   └── routes/                  #   Controllers delgados: auth, events, artists, venues
└── main.py                      # Composition root: arma la app y monta los routers
```

> El flujo de una petición: **route** (traduce HTTP → comando) → **use case** (orquesta vía ports) → **repository** (SQLAlchemy/PostGIS) → **mapper** (ORM → entidad) → **presenter** (entidad → schema Pydantic) → respuesta JSON. Los errores de negocio fluyen como `DomainError` y se mapean a HTTP en el borde.

### 6.4 Estructura de carpetas del frontend

```
frontend/src/app/
├── core/
│   ├── models/                  # Interfaces TS espejo de los schemas del backend
│   ├── services/                # AuthService, EventService, VenueService, GeolocationService
│   ├── guards/organizer.guard.ts# Protege las rutas /organizer por rol
│   └── interceptors/auth.interceptor.ts
├── features/
│   ├── map/                     # Mapa MapLibre — ruta por defecto ''
│   ├── events/
│   │   ├── event-panel/         # Panel derecho: lista de eventos top ⇄ detalle
│   │   └── event-popup/         # (el popup se renderiza hoy desde map.component)
│   ├── search/search-bar.component.ts
│   ├── auth/auth.component.ts   # ruta 'auth' — login + registro
│   └── organizer/
│       ├── organizer-dashboard/ # ruta 'organizer'
│       └── event-form/          # rutas 'organizer/events/new' y '…/:id/edit'
├── app.routes.ts                # rutas lazy con loadComponent
└── app.config.ts                # providers (router, HttpClient + interceptor)
```

**Rutas registradas:**

| Ruta | Componente | Guard |
|---|---|---|
| `''` | `MapComponent` | — |
| `auth` | `AuthComponent` | — |
| `organizer` | `OrganizerDashboardComponent` | `organizerGuard` |
| `organizer/events/new` | `EventFormComponent` | `organizerGuard` |
| `organizer/events/:id/edit` | `EventFormComponent` | `organizerGuard` |
| `**` | redirect a `''` | — |

> La URL base de la API vive en `src/environments/environment.ts` (`http://localhost:8000/api`).

---

## 7. Modelos de Datos

El dominio se representa en **tres formas** según la capa de Clean Architecture, cada una con una responsabilidad distinta:

1. **Entidades de dominio** (`app/domain/entities.py`) — dataclasses puras de Python, sin dependencias de framework. Son la fuente de verdad de las reglas de negocio.
2. **Schemas Pydantic** (`app/api/schemas/`) — DTOs de entrada/salida HTTP con validación; exponen *presenters* (`from_entity`) y se reflejan como interfaces TypeScript en el frontend Angular vía el esquema OpenAPI.
3. **Modelos SQLAlchemy** (`app/infrastructure/persistence/models/`) — detalle de persistencia (tablas + GeoAlchemy2); un módulo de `mappers` traduce hacia/desde las entidades.

> Los ejemplos de código a continuación muestran la **forma de los datos** (campos y tipos). En el código real, los `EventBase`/`ArtistBase`/etc. con `BaseModel` corresponden a los schemas Pydantic de la capa API; las entidades de dominio equivalentes son dataclasses con los mismos campos pero sin Pydantic.

### 7.1 Event

```python
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from enum import Enum
from typing import Optional

class EventCategory(str, Enum):
    music = "music"
    visual_art = "visual_art"
    theater = "theater"
    dance = "dance"
    spoken_word = "spoken_word"
    cinema = "cinema"
    festival = "festival"
    workshop = "workshop"
    street_performance = "street_performance"

class EventStatus(str, Enum):
    draft = "draft"
    pending = "pending"        # publicado por el organizador, esperando moderación
    published = "published"
    cancelled = "cancelled"
    past = "past"

class EventBase(BaseModel):
    title: str
    category: EventCategory
    start_date: datetime
    description: Optional[str] = None
    end_date: Optional[datetime] = None
    cover_image: Optional[str] = None
    gallery: list[str] = []
    video_url: Optional[str] = None
    ticket_url: Optional[HttpUrl] = None
    ticket_price: Optional[float] = None
    currency: str = "MXN"      # ⚠️ default heredado; los datos sembrados usan PEN (Lima)
    is_free: bool = False
    capacity: Optional[int] = None
    tags: list[str] = []

class EventCreate(EventBase):
    venue_id: str
    artist_ids: list[str]

class EventResponse(EventBase):
    id: str
    status: EventStatus
    venue: "VenueBase"
    artists: list["ArtistSummary"]
    organizer_id: str
    distance_meters: Optional[float] = None  # solo en queries nearby
    created_at: datetime
    updated_at: datetime
```

### 7.2 Artist

```python
class SocialLinks(BaseModel):
    instagram: Optional[HttpUrl] = None
    spotify: Optional[HttpUrl] = None
    soundcloud: Optional[HttpUrl] = None
    youtube: Optional[HttpUrl] = None
    website: Optional[HttpUrl] = None

class ArtistBase(BaseModel):
    name: str
    slug: str
    bio: str
    category: str
    genres: list[str] = []
    profile_image: str
    gallery: list[str] = []
    social_links: SocialLinks = SocialLinks()
    audio_preview_url: Optional[str] = None

class ArtistSummary(BaseModel):
    id: str
    name: str
    profile_image: str
    genres: list[str]

class ArtistResponse(ArtistBase):
    id: str
    follower_count: int
    is_verified: bool
    verified_at: Optional[datetime] = None
    upcoming_events: list["EventResponse"] = []
```

### 7.3 Venue

```python
class Coordinates(BaseModel):
    longitude: float
    latitude: float

class VenueBase(BaseModel):
    name: str
    address: str
    city: str
    country: str
    coordinates: Coordinates
    description: Optional[str] = None
    google_maps_url: Optional[HttpUrl] = None
    capacity: Optional[int] = None
    accessibility: list[str] = []
    transit_info: list[str] = []

class VenueResponse(VenueBase):
    id: str
    upcoming_event_count: int
```

### 7.4 User

```python
class UserRole(str, Enum):
    attendee = "attendee"
    artist = "artist"
    organizer = "organizer"
    admin = "admin"

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    avatar: Optional[str] = None
    role: UserRole
    is_active: bool = True
    notifications_enabled: bool = True
    saved_event_ids: list[str] = []
    followed_artist_ids: list[str] = []
```

> **Preferencias de ubicación:** la entidad de dominio `User` no anida un objeto
> `LocationPreferences`; guarda campos planos `pref_lat`, `pref_lng` y `pref_radius_km` (default
> `5`), y expone la propiedad derivada `User.location_preference -> Coordinates | None`.

```python
# app/domain/entities.py — reglas de negocio en la entidad
class User:
    def has_any_role(self, *roles: UserRole) -> bool: ...
    def can_manage_event(self, organizer_id: str) -> bool:
        """Un evento lo administra su organizador o un admin."""

class Event:
    @property
    def is_visible(self) -> bool:
        """Los borradores nunca se exponen por endpoints públicos de lectura."""
```

### 7.5 Modelos de Base de Datos (SQLAlchemy + GeoAlchemy2)

```python
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Enum as SAEnum
from geoalchemy2 import Geometry
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class EventModel(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String, nullable=False)
    category = Column(SAEnum(EventCategory), nullable=False)
    status = Column(SAEnum(EventStatus), default=EventStatus.draft)
    # Columna geoespacial — índice GiST aplicado en migración Alembic
    coordinates = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)
    is_free = Column(Boolean, default=False)
    ticket_price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
```

---

## 8. API — Endpoints Clave

Todos montados bajo el prefijo `/api`. Documentación interactiva en `/docs` (Swagger) y
`/redoc`; `/` redirige a `/docs`.

### Auth

| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/api/auth/register` | Registro → `TokenResponse` (201) |
| `POST` | `/api/auth/login` | Login → access + refresh token |
| `POST` | `/api/auth/refresh` | Renovar tokens a partir del refresh token |
| `GET` | `/api/auth/me` | Usuario autenticado actual |

### Eventos

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/events/nearby` | Eventos dentro de radio geoespacial |
| `GET` | `/api/events/mine` | Eventos del organizador autenticado |
| `GET` | `/api/events/:id` | Detalle de evento |
| `POST` | `/api/events` | Crear evento (auth: organizer/admin) |
| `PATCH` | `/api/events/:id` | Actualizar evento (auth: dueño o admin) |
| `DELETE` | `/api/events/:id` | Eliminar evento (auth: dueño o admin) |
| `POST` | `/api/events/:id/save` | Guardar evento en favoritos (204) |
| `DELETE` | `/api/events/:id/save` | Quitar de favoritos (204) |
| `GET` | `/api/events` | 🚧 Listar/buscar eventos con filtros — **pendiente**; lo necesita la barra de búsqueda global (§4.4) |

### Venues

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/venues` | Listar venues (alimenta el selector del formulario de evento) |
| `GET` | `/api/venues/:id` | Detalle de venue |
| `POST` | `/api/venues` | Crear venue (auth: organizer/admin) |

### Query Geoespacial (events/nearby)

Parámetros implementados (todos en `snake_case`, igual que la respuesta):

```
GET /api/events/nearby?
  lat=-12.0464&         // requerido, -90..90
  lng=-77.0428&         // requerido, -180..180
  radius=5000&          // metros, 100..100000 (default 5000)
  category=music&       // opcional, EventCategory
  is_free=false&        // opcional
  limit=50              // 1..100 (default 50)
```

🚧 Filtros por rango de fechas (`start_date`/`end_date`) aún no implementados.

**Respuesta** (`NearbyEventsResponse` → items de tipo `EventSummary`, aligerado para el mapa):

```json
{
  "events": [
    {
      "id": "...",
      "title": "...",
      "category": "music",
      "status": "published",
      "start_date": "2026-07-25T21:00:00",
      "cover_image": "...",
      "is_free": false,
      "ticket_price": 60,
      "currency": "PEN",
      "coordinates": { "longitude": -77.0428, "latitude": -12.0464 },
      "distance_meters": 1240,
      "venue_name": "Sargento Pimienta",
      "artist_names": ["..."]
    }
  ],
  "total": 23,
  "next_cursor": null
}
```

> El detalle completo (`GET /api/events/:id`) devuelve `EventResponse`, que sí incluye
> `description`, `gallery`, `video_url`, `tags`, el `venue` completo y las `artists` como
> objetos `ArtistSummary`.

### Artistas

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/artists/:id` | Perfil de artista |
| `POST` | `/api/artists` | Crear perfil artístico |
| `POST` | `/api/artists/:id/follow` | Seguir artista |
| `DELETE` | `/api/artists/:id/follow` | Dejar de seguir |

---

## 9. Requerimientos No Funcionales

### Performance

- **LCP (Largest Contentful Paint):** < 2.5s
- **Carga inicial del mapa:** < 1.5s
- **Respuesta de API geoespacial:** < 200ms (con índice GiST en PostGIS) ✅
- **Eventos en caché (Redis):** TTL 5 min por geohash 🚧 (Redis levantado, caché sin implementar)
- **Imágenes:** WebP con lazy loading (`loading="lazy"` ya aplicado en la galería);
  thumbnails redimensionados en CDN 🚧

### Escalabilidad

- Índice GiST en columna de coordenadas para queries geoespaciales eficientes ✅
- Paginación por cursor (no offset) para listas de eventos 🚧 — `NearbyEventsResponse` ya
  reserva el campo `next_cursor`, pero hoy solo se aplica `limit`
- Rate limiting: 100 req/min públicos, 20 req/min autenticados 🚧 — `slowapi` está instalado y
  el `Limiter` registrado en `main.py`, pero **ningún endpoint declara `@limiter.limit`** todavía

### Accesibilidad 🚧

*Objetivo, aún sin auditar.*

- WCAG 2.1 AA compliance
- Navegación por teclado completa en panel lateral
- Contraste mínimo 4.5:1 en texto
- Labels ARIA en todos los controles del mapa
- Modo alto contraste disponible

### Seguridad

- Autenticación JWT con refresh tokens (`python-jose`, access token 15 min, refresh token 7 días) ✅
- Validación y sanitización de inputs con **Pydantic v2** (automático en FastAPI) ✅
- CORS configurado para dominios permitidos (`BACKEND_CORS_ORIGINS`) ✅
- Autorización por rol en el borde HTTP: `require_role(...)` en `api/deps.py` ✅
- Rate limiting con `slowapi` por IP en endpoints de publicación 🚧 (ver Escalabilidad)
- Moderación de contenido antes de publicar (estado `pending`) 🚧

---

## 10. Flujos de Usuario

### Flujo 1: Descubrimiento de evento

```
Abrir app
  → Mapa centrado en ubicación del usuario
  → Ver marcadores de eventos cercanos
  → Aplicar filtro "Música" + "Esta semana"
  → Click en marcador
  → Popup con info básica
  → Click "Ver detalles"
  → Panel lateral se abre con info completa
  → Reproducir preview de audio
  → Click "Obtener Entradas"
  → Redirigir a link de ticketing externo
```

### Flujo 2: Publicación de evento

```
Login como organizador
  → Click "Publicar Evento" (botón flotante)
  → Formulario paso a paso (stepper)
  → Seleccionar venue en el mapa
  → Agregar artistas
  → Upload de multimedia
  → Preview del popup
  → Publicar → Estado "pendiente moderación"
  → Aprobación → Evento visible en mapa
```

### Flujo 3: Seguimiento de artista

```
Panel lateral → Sección "Artistas"
  → Click en card de artista
  → Ver perfil expandido
  → Click "Seguir"
  → Confirmación: "Recibirás notificaciones de nuevos eventos"
  → Push notification cuando artista publique evento nuevo
```

---

## 11. Roadmap de Desarrollo

### Fase 1 — MVP (8 semanas)

- [x] Setup monorepo: Angular app + FastAPI app + Docker Compose (Postgres+PostGIS, Redis)
- [x] Modelos SQLAlchemy + migraciones Alembic (events, venues, artists, users) + `seed.py`
- [x] Auth endpoints FastAPI: register, login, refresh token, me
- [x] Angular: standalone components, routing lazy, guard por rol, interceptor JWT
- [x] Mapa base con MapLibre GL + geolocalización del navegador
- [x] Endpoint `GET /api/events/nearby` con query PostGIS
- [x] Marcadores en mapa por categoría
- [ ] Clustering de marcadores
- [x] Popup del evento (marcador → tarjeta HTML custom sobre el mapa)
- [x] Panel lateral (lista de eventos top ⇄ detalle, responsive/bottom sheet)
- [x] Filtro por radio y categoría + círculo de radio auto-ajustado
- [ ] Deploy inicial: Netlify (Angular) + Railway (FastAPI + Postgres + Redis)

### Fase 2 — Core Features (6 semanas)

- [ ] Perfiles de artista completos con galería y social links *(backend listo, falta el frontend)*
- [ ] Upload multimedia: endpoint FastAPI con `python-multipart` → S3/R2 *(hoy solo por URL)*
- [ ] Búsqueda global con autocomplete *(UI hecha; falta el endpoint `GET /api/events`)*
- [ ] Sistema de usuarios: guardar eventos, seguir artistas *(endpoints listos, falta UI)*
- [ ] Notificaciones push: Web Push API + Celery worker en Python
- [x] Panel de administración para organizadores (dashboard + alta/edición de eventos)

### Fase 3 — Enhancement (4 semanas)

- [ ] Reproductor de audio en panel lateral (`AudioPlayerService` con Howler.js)
- [ ] Galería de imágenes swipeable (Angular CDK Drag o directiva custom)
- [ ] Recomendaciones basadas en historial (endpoint FastAPI con lógica de scoring)
- [ ] PWA: Angular Service Worker (`@angular/pwa`) para modo offline
- [ ] SEO: pre-rendering con Angular Universal o páginas compartibles via meta tags dinámicos
- [ ] Internacionalización: Angular i18n para ES/EN

### Fase 4 — Monetización (futura)

- [ ] Plan "Featured Event" (eventos destacados en mapa)
- [ ] Perfil de artista verificado (badge)
- [ ] Analytics para organizadores (views, clicks, conversiones)
- [ ] Integración nativa de ticketing

---

## 12. Consideraciones de Contenido

- Los eventos pueden tener multimedia embebida de Spotify, SoundCloud, YouTube, Vimeo, Bandcamp
- Se respetan las embed APIs de cada plataforma (no se descarga contenido)
- Los artistas pueden vincular su perfil de Spotify para mostrar tracks directamente
- Las imágenes se almacenan internamente; el audio es siempre embebido desde origen

---

*ZoomArtists v1.2 — Specs by Claude · Julio 2026*

*Rev. 1.1: backend refactorizado a Clean Architecture (capas domain/application/infrastructure/api) + documentación Swagger/OpenAPI en `/docs`.*

*Rev. 1.2 (2026-07-23): sincronización con el código. Stack frontend real (Angular 21 +
MapLibre GL directo, Tailwind v4, sin Angular Material/NgRx/Mapbox); estructura y rutas del
frontend (§6.4); área de organizador (§4.5); enums y campos reales de los modelos (§7);
tabla de endpoints completa con Auth y Venues (§8); parámetros y respuesta reales de
`/events/nearby`; marcado de estado ✅/🚧 en features y requerimientos no funcionales;
roadmap actualizado al avance real.*
