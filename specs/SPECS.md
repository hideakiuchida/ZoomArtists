# ZoomArtists — Especificaciones de Producto v1.0

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

- Mapa de pantalla completa renderizado con **Mapbox GL JS** o **Leaflet + OpenStreetMap**
- Detección automática de geolocalización del usuario (con permiso)
- Selector de radio de distancia: 1 km / 5 km / 10 km / 25 km / Sin límite
- Marcadores agrupados (clustering) que se separan al hacer zoom
- Marcadores con íconos visuales diferenciados por categoría de evento
- Animaciones suaves al desplazarse y hacer zoom
- Controles: zoom, centrar en ubicación actual, cambiar estilo de mapa (claro/oscuro/artístico)
- Filtros flotantes sobre el mapa: por categoría, fecha, precio (gratis / de pago), horario

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

Panel deslizable desde la derecha (ancho: 380px en desktop, 100% en mobile):

**Secciones del panel:**

#### Header del Evento
- Imagen de portada a todo el ancho del panel con gradiente inferior
- Badge de categoría (ej: 🎭 TEATRO)
- Nombre del evento en tipografía grande
- Venue con link a Google Maps
- Fecha, hora y duración estimada
- Precio / "Entrada libre"
- Botones: `[Obtener Entradas]` `[♥]` `[↗ Compartir]`

#### Artistas
- Cards horizontales con foto del artista, nombre, género/disciplina
- Click en card de artista expande mini-perfil con:
  - Bio corta (2-3 líneas)
  - Tags de género/estilo
  - Links a redes sociales (Instagram, Spotify, SoundCloud, YouTube)
  - Botón `[Seguir Artista]`

#### Contenido Multimedia
- Reproductor de audio embebido (preview de tracks si aplica)
- Galería de imágenes del artista o eventos anteriores (scroll horizontal)
- Video embed (YouTube/Vimeo) si está disponible
- Reproducción automática de preview al abrir el panel (con ícono de mute visible)

#### Detalles del Venue
- Mapa en miniatura del venue dentro del panel
- Dirección completa
- Información de accesibilidad
- Transporte cercano (metro, bus)
- Capacidad y aforo

#### Más Eventos en este Venue
- Scroll horizontal de cards de próximos eventos en el mismo lugar

#### Footer del Panel
- `[← Cerrar]` en esquina superior izquierda del panel
- Fondo del panel: oscuro semitransparente con efecto blur (glassmorphism)

### 4.4 Barra de Búsqueda Global

- Barra flotante centrada en la parte superior del mapa
- Búsqueda por: nombre de evento, artista, venue, género, ciudad
- Autocompletado con resultados en tiempo real
- Al seleccionar resultado: el mapa vuela (fly-to) hacia la ubicación

### 4.5 Publicación de Eventos (para artistas/organizadores)

Formulario de creación de evento:

1. **Información básica:** Nombre, categoría, descripción
2. **Fecha y hora:** Selector de fecha/hora, duración, recurrencia
3. **Ubicación:** Búsqueda de venue o pin manual en mapa
4. **Artistas:** Agregar artistas (con lookup si ya tienen perfil) o crear nuevo
5. **Multimedia:** Upload de imagen de portada, galería, links de audio/video
6. **Entradas:** Precio, link de venta, aforo máximo
7. **Preview:** Vista previa del popup y panel antes de publicar

### 4.6 Perfiles de Artista

- Página de perfil dedicada accesible desde el panel lateral
- Portfolio multimedia: tracks, videos, galería
- Historial de eventos pasados y próximos
- Botón de "Seguir" para notificaciones de nuevos eventos
- Links a redes sociales y plataformas de streaming

### 4.7 Sistema de Usuarios

| Rol | Capacidades |
|---|---|
| **Visitante** | Ver mapa, popup, panel de detalles, buscar |
| **Usuario registrado** | + Guardar eventos, seguir artistas, recibir notificaciones |
| **Artista** | + Crear perfil artístico, asociarse a eventos |
| **Organizador** | + Publicar y administrar eventos |
| **Admin** | + Moderar contenido, aprobar publicaciones |

---

## 5. Diseño UI/UX

### 5.1 Principios de Diseño

- **Inmersivo:** El mapa ocupa el 100% del viewport; la UI flota sobre él
- **Oscuro por defecto:** Tema oscuro con acentos en colores vibrantes según categoría
- **Fluidez:** Transiciones suaves (300-500ms) en todas las interacciones
- **Mobile-first:** Diseño responsivo con gestos touch nativos

### 5.2 Paleta de Colores por Categoría

| Categoría | Color de acento |
|---|---|
| Música | `#7C3AED` — Violeta |
| Arte Visual | `#F59E0B` — Ámbar |
| Teatro / Danza | `#EC4899` — Rosa |
| Cine | `#3B82F6` — Azul |
| Spoken Word | `#10B981` — Esmeralda |
| Festival | `#EF4444` — Rojo |

### 5.3 Layout General

```
┌─────────────────────────────────────────────────────────┐
│  [Logo]   [🔍 Buscar eventos, artistas, venues...]  [👤]│  ← Header flotante
├─────────────────────────────────────────────────────────┤
│                                                         │
│   [🎵] [🎨] [🎭] [🎬] [All]  ←── Filtros flotantes     │
│                                                         │
│                    M A P A                              │
│              (pantalla completa)           ┌──────────┐ │
│                                            │  PANEL   │ │
│        📍📍   📍                           │ LATERAL  │ │
│                  📍📍                      │ DERECHO  │ │
│           📍                               │          │ │
│                                            │          │ │
│                                            └──────────┘ │
│  [Radio: 5km ▾]           [🎯 Mi ubicación]             │
└─────────────────────────────────────────────────────────┘
```

### 5.4 Estados y Micro-interacciones

- **Marcador hover:** Escala a 1.2x con sombra de color de categoría + nombre del evento en tooltip
- **Marcador activo:** Pulso (ping animation) en el color de la categoría
- **Panel lateral:** Slide-in desde la derecha con ease-out, backdrop blur en el mapa
- **Carga de eventos:** Skeleton screens mientras cargan los datos
- **Radio de distancia:** Círculo translúcido visible en el mapa mostrando el área de búsqueda
- **Fly-to:** Animación de vuelo suave al centrar en un evento desde búsqueda

---

## 6. Arquitectura Técnica

### 6.1 Stack Tecnológico Recomendado

**Frontend — Angular**
- **Framework:** Angular 17+ con Standalone Components y Signals
- **Mapa:** `ngx-mapbox-gl` (wrapper oficial de Mapbox GL JS para Angular)
- **Estilos:** Tailwind CSS + Angular Material (componentes base: dialogs, overlays, sliders)
- **Animaciones:** Angular Animations API (`@angular/animations`) + CSS custom transitions
- **Estado:** Angular Signals + `effect()` para reactividad; NgRx Signal Store para estado complejo
- **HTTP:** `HttpClient` con interceptors para auth y error handling
- **Audio:** Howler.js (integrado en servicio Angular `AudioPlayerService`)
- **Formularios:** Reactive Forms con validadores custom
- **Routing:** Angular Router con lazy loading por módulo funcional

**Backend — Python**
- **Framework:** **FastAPI** — async, alto rendimiento, auto-genera OpenAPI docs (Swagger UI en `/docs`, ReDoc en `/redoc`)
- **Arquitectura:** **Clean Architecture** (ver 6.2) — reglas de negocio independientes del framework
- **ORM:** SQLAlchemy 2.0 (async) + **GeoAlchemy2** para queries PostGIS
- **Migraciones:** Alembic
- **Validación:** Pydantic v2 (integrado en FastAPI)
- **Base de Datos:** PostgreSQL con extensión **PostGIS** (queries geoespaciales)
- **Cache:** Redis con `redis-py` async — eventos por geohash, sesiones
- **Storage:** AWS S3 o Cloudflare R2 con `boto3` (imágenes, audio)
- **Tareas en background:** Celery + Redis Broker (envío de notificaciones push)
- **Server:** Uvicorn + Gunicorn (producción)
- **CDN:** Cloudflare

**Autenticación**
- Backend: `python-jose` para JWT access/refresh tokens + `bcrypt` para hashing de contraseñas
- Providers OAuth: Google, Apple (via `authlib`)
- Frontend: Interceptor HTTP en Angular + guard de rutas por rol

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

class EventStatus(str, Enum):
    draft = "draft"
    published = "published"
    cancelled = "cancelled"
    past = "past"

class EventBase(BaseModel):
    title: str
    description: str
    category: EventCategory
    start_date: datetime
    end_date: datetime
    cover_image: str
    gallery: list[str] = []
    ticket_url: Optional[HttpUrl] = None
    ticket_price: Optional[float] = None
    currency: Optional[str] = None
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

class LocationPreferences(BaseModel):
    default_coordinates: Coordinates
    default_radius_km: int = 5

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    avatar: Optional[str] = None
    role: UserRole
    notifications_enabled: bool = True
    location_preferences: Optional[LocationPreferences] = None
    saved_event_ids: list[str] = []
    followed_artist_ids: list[str] = []
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

### Eventos

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/events` | Listar eventos con filtros |
| `GET` | `/api/events/nearby` | Eventos dentro de radio geoespacial |
| `GET` | `/api/events/:id` | Detalle de evento |
| `POST` | `/api/events` | Crear evento (auth: organizer) |
| `PATCH` | `/api/events/:id` | Actualizar evento |
| `DELETE` | `/api/events/:id` | Eliminar evento |

### Query Geoespacial (events/nearby)

```
GET /api/events/nearby?
  lat=19.4326&
  lng=-99.1332&
  radius=5000&          // metros
  category=music&
  startDate=2026-06-14&
  endDate=2026-06-21&
  isFree=false&
  limit=50&
  offset=0
```

**Respuesta:**
```json
{
  "events": [
    {
      "id": "...",
      "title": "...",
      "category": "music",
      "startDate": "...",
      "coordinates": [-99.1332, 19.4326],
      "distanceMeters": 1240,
      "coverImage": "...",
      "isFree": false,
      "ticketPrice": 150,
      "venue": { "name": "Foro Indie Rocks", "address": "..." },
      "artists": [{ "id": "...", "name": "...", "profileImage": "..." }]
    }
  ],
  "total": 23,
  "hasMore": false
}
```

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
- **Respuesta de API geoespacial:** < 200ms (con índice GiST en PostGIS)
- **Eventos en caché (Redis):** TTL 5 min por geohash
- **Imágenes:** WebP con lazy loading; thumbnails redimensionados en CDN

### Escalabilidad

- Paginación por cursor (no offset) para listas de eventos
- Rate limiting: 100 req/min para endpoints públicos, 20 req/min para autenticados
- Índice GiST en columna de coordenadas para queries geoespaciales eficientes

### Accesibilidad

- WCAG 2.1 AA compliance
- Navegación por teclado completa en panel lateral
- Contraste mínimo 4.5:1 en texto
- Labels ARIA en todos los controles del mapa
- Modo alto contraste disponible

### Seguridad

- Autenticación JWT con refresh tokens (`python-jose`, access token 15 min, refresh token 7 días)
- Validación y sanitización de inputs con **Pydantic v2** (automático en FastAPI)
- Rate limiting con `slowapi` (wrapper de limits para FastAPI) por IP en endpoints de publicación
- Moderación de contenido antes de publicar (manual o con moderación AI)
- CORS configurado para dominios permitidos

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

- [ ] Setup monorepo: Angular app + FastAPI app + Docker Compose (Postgres+PostGIS, Redis)
- [ ] Modelos SQLAlchemy + migraciones Alembic (events, venues, artists, users)
- [ ] Auth endpoints FastAPI: register, login, refresh token
- [ ] Angular: estructura de módulos, routing, AuthGuard, interceptor JWT
- [ ] Mapa base con `ngx-mapbox-gl` + geolocalización del navegador
- [ ] Endpoint `GET /api/events/nearby` con query PostGIS
- [ ] Marcadores en mapa + clustering por categoría
- [ ] Popup del evento (Angular overlay/CDK)
- [ ] Panel lateral básico (Angular Animation slide-in)
- [ ] Filtro por radio y categoría
- [ ] Deploy inicial: Netlify (Angular) + Railway (FastAPI + Postgres + Redis)

### Fase 2 — Core Features (6 semanas)

- [ ] Perfiles de artista completos con galería y social links
- [ ] Upload multimedia: endpoint FastAPI con `python-multipart` → S3/R2
- [ ] Búsqueda global con autocomplete (Angular `HttpClient` + debounce con RxJS)
- [ ] Sistema de usuarios: guardar eventos, seguir artistas (NgRx Signal Store)
- [ ] Notificaciones push: Web Push API + Celery worker en Python
- [ ] Panel de administración para organizadores (módulo lazy-loaded en Angular)

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

*ZoomArtists v1.1 — Specs by Claude · Junio 2026*
*Rev. 1.1: backend refactorizado a Clean Architecture (capas domain/application/infrastructure/api) + documentación Swagger/OpenAPI en `/docs`.*
