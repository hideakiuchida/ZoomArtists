"""Seed the database with sample venues, artists, and events around Mexico City.

Run with:  uv run python seed.py
Re-running wipes the existing events/artists/venues and the demo organizer first.
"""

import asyncio
import hashlib
from datetime import UTC, datetime, timedelta

from geoalchemy2.elements import WKTElement
from sqlalchemy import delete

from app.infrastructure.persistence.database import AsyncSessionLocal
from app.infrastructure.persistence.models.artist import Artist
from app.infrastructure.persistence.models.event import (
    Event,
    EventArtist,
    EventCategory,
    EventStatus,
)
from app.infrastructure.persistence.models.user import User, UserRole
from app.infrastructure.persistence.models.venue import Venue
from app.infrastructure.security.password_hasher import BcryptPasswordHasher

hash_password = BcryptPasswordHasher().hash


def point(lng: float, lat: float) -> WKTElement:
    return WKTElement(f"POINT({lng} {lat})", srid=4326)


def img(seed: str, w: int = 800, h: int = 600) -> str:
    # Real, themed photos via loremflickr. A deterministic `lock` derived from the
    # seed string keeps each image stable across re-seeds and page reloads.
    lock = int(hashlib.md5(seed.encode()).hexdigest(), 16) % 10_000
    return f"https://loremflickr.com/{w}/{h}/concert,art,culture?lock={lock}"


# ── Venues around the historic center of CDMX (19.4326, -99.1332) ─────────────
VENUES = [
    {
        "key": "indie_rocks",
        "name": "Foro Indie Rocks!",
        "address": "Zacatecas 39, Roma Norte",
        "city": "Ciudad de México",
        "country": "México",
        "lng": -99.1580, "lat": 19.4180,
        "capacity": 350,
        "accessibility": ["Acceso para silla de ruedas"],
        "transit_info": ["Metro Insurgentes (L1)", "Metrobús Durango"],
    },
    {
        "key": "bellas_artes",
        "name": "Palacio de Bellas Artes",
        "address": "Av. Juárez s/n, Centro Histórico",
        "city": "Ciudad de México",
        "country": "México",
        "lng": -99.1413, "lat": 19.4352,
        "capacity": 1000,
        "accessibility": ["Acceso para silla de ruedas", "Audioguía"],
        "transit_info": ["Metro Bellas Artes (L2, L8)"],
    },
    {
        "key": "teatro_helenico",
        "name": "Teatro Helénico",
        "address": "Av. Revolución 1500, Guadalupe Inn",
        "city": "Ciudad de México",
        "country": "México",
        "lng": -99.1890, "lat": 19.3580,
        "capacity": 430,
        "accessibility": ["Acceso para silla de ruedas"],
        "transit_info": ["Metro Barranca del Muerto (L7)"],
    },
    {
        "key": "galeria_omr",
        "name": "Galería OMR",
        "address": "Córdoba 100, Roma Norte",
        "city": "Ciudad de México",
        "country": "México",
        "lng": -99.1620, "lat": 19.4200,
        "capacity": 120,
        "accessibility": ["Entrada a nivel de calle"],
        "transit_info": ["Metrobús Álvaro Obregón"],
    },
    {
        "key": "cineteca",
        "name": "Cineteca Nacional",
        "address": "Av. México Coyoacán 389, Xoco",
        "city": "Ciudad de México",
        "country": "México",
        "lng": -99.1660, "lat": 19.3650,
        "capacity": 250,
        "accessibility": ["Acceso para silla de ruedas", "Subtítulos"],
        "transit_info": ["Metro Coyoacán (L3)"],
    },
    {
        "key": "monumento_rev",
        "name": "Monumento a la Revolución",
        "address": "Plaza de la República s/n, Tabacalera",
        "city": "Ciudad de México",
        "country": "México",
        "lng": -99.1540, "lat": 19.4360,
        "capacity": 5000,
        "accessibility": ["Espacio abierto"],
        "transit_info": ["Metro Revolución (L2)", "Metrobús Plaza de la República"],
    },
    # ── Venues in Lima, Perú (center ~ -12.0464, -77.0428) ────────────────────
    {
        "key": "la_noche",
        "name": "La Noche de Barranco",
        "address": "Bolognesi 307, Barranco",
        "city": "Lima",
        "country": "Perú",
        "lng": -77.0210, "lat": -12.1490,
        "capacity": 400,
        "accessibility": ["Entrada a nivel de calle"],
        "transit_info": ["Metropolitano Estación Bulevar"],
    },
    {
        "key": "gran_teatro",
        "name": "Gran Teatro Nacional",
        "address": "Av. Javier Prado Este 2225, San Borja",
        "city": "Lima",
        "country": "Perú",
        "lng": -77.0050, "lat": -12.0822,
        "capacity": 1400,
        "accessibility": ["Acceso para silla de ruedas", "Audioguía"],
        "transit_info": ["Metro Línea 1 Estación La Cultura"],
    },
    {
        "key": "mali",
        "name": "Museo de Arte de Lima (MALI)",
        "address": "Paseo Colón 125, Cercado de Lima",
        "city": "Lima",
        "country": "Perú",
        "lng": -77.0370, "lat": -12.0608,
        "capacity": 300,
        "accessibility": ["Acceso para silla de ruedas"],
        "transit_info": ["Metropolitano Estación Estadio Nacional"],
    },
    {
        "key": "teatro_municipal_lima",
        "name": "Teatro Municipal de Lima",
        "address": "Jr. Ica 377, Cercado de Lima",
        "city": "Lima",
        "country": "Perú",
        "lng": -77.0340, "lat": -12.0490,
        "capacity": 800,
        "accessibility": ["Acceso para silla de ruedas"],
        "transit_info": ["Estación Central Metropolitano"],
    },
    {
        "key": "cc_ricardo_palma",
        "name": "Centro Cultural Ricardo Palma",
        "address": "Av. Larco 770, Miraflores",
        "city": "Lima",
        "country": "Perú",
        "lng": -77.0290, "lat": -12.1215,
        "capacity": 220,
        "accessibility": ["Entrada a nivel de calle"],
        "transit_info": ["Metropolitano Estación Ricardo Palma"],
    },
    {
        "key": "parque_exposicion",
        "name": "Parque de la Exposición",
        "address": "Av. 28 de Julio, Cercado de Lima",
        "city": "Lima",
        "country": "Perú",
        "lng": -77.0370, "lat": -12.0660,
        "capacity": 6000,
        "accessibility": ["Espacio abierto"],
        "transit_info": ["Estación Central Metropolitano"],
    },
]


# ── Artists ───────────────────────────────────────────────────────────────────
ARTISTS = [
    {
        "key": "lng_division",
        "name": "Long Division",
        "category": "music",
        "genres": ["indie rock", "shoegaze"],
        "bio": "Banda mexicana de indie rock con texturas de shoegaze y letras introspectivas.",
        "social": {"instagram": "https://instagram.com/longdivision", "spotify": "https://open.spotify.com/artist/longdivision"},
        "audio": "https://example.com/preview/longdivision.mp3",
    },
    {
        "key": "ana_torres",
        "name": "Ana Torres",
        "category": "visual_art",
        "genres": ["arte contemporáneo", "instalación"],
        "bio": "Artista visual que explora la memoria urbana a través de instalaciones lumínicas.",
        "social": {"instagram": "https://instagram.com/anatorres.art"},
        "audio": None,
    },
    {
        "key": "cia_nado",
        "name": "Compañía Nado",
        "category": "dance",
        "genres": ["danza contemporánea"],
        "bio": "Colectivo de danza contemporánea fundado en 2015 en la Ciudad de México.",
        "social": {"instagram": "https://instagram.com/companianado", "youtube": "https://youtube.com/@companianado"},
        "audio": None,
    },
    {
        "key": "el_mato",
        "name": "El Mató a un Policía Motorizado",
        "category": "music",
        "genres": ["indie rock", "noise pop"],
        "bio": "Banda argentina de culto del indie latinoamericano.",
        "social": {"spotify": "https://open.spotify.com/artist/elmato", "instagram": "https://instagram.com/elmato"},
        "audio": "https://example.com/preview/elmato.mp3",
    },
    {
        "key": "rivera_quartet",
        "name": "Rivera Quartet",
        "category": "music",
        "genres": ["jazz", "bossa nova"],
        "bio": "Cuarteto de jazz con influencias brasileñas, residentes en la Roma.",
        "social": {"spotify": "https://open.spotify.com/artist/riveraquartet"},
        "audio": "https://example.com/preview/rivera.mp3",
    },
    {
        "key": "teatro_linea",
        "name": "Teatro Línea de Sombra",
        "category": "theater",
        "genres": ["teatro documental"],
        "bio": "Compañía de teatro contemporáneo reconocida por su trabajo documental.",
        "social": {"instagram": "https://instagram.com/lineadesombra"},
        "audio": None,
    },
    # ── Peruvian artists ──────────────────────────────────────────────────────
    {
        "key": "los_mirlos",
        "name": "Los Mirlos",
        "category": "music",
        "genres": ["cumbia amazónica", "chicha"],
        "bio": "Leyenda de la cumbia amazónica peruana, activos desde los años 70.",
        "social": {"spotify": "https://open.spotify.com/artist/losmirlos", "instagram": "https://instagram.com/losmirlosoficial"},
        "audio": "https://example.com/preview/losmirlos.mp3",
    },
    {
        "key": "susana_baca",
        "name": "Susana Baca",
        "category": "music",
        "genres": ["música afroperuana", "landó"],
        "bio": "Cantante y compositora ganadora del Grammy, embajadora de la música afroperuana.",
        "social": {"spotify": "https://open.spotify.com/artist/susanabaca", "youtube": "https://youtube.com/@susanabaca"},
        "audio": "https://example.com/preview/susanabaca.mp3",
    },
    {
        "key": "novalima",
        "name": "Novalima",
        "category": "music",
        "genres": ["electrónica", "afrobeat", "fusión"],
        "bio": "Colectivo limeño que fusiona ritmos afroperuanos con producción electrónica.",
        "social": {"spotify": "https://open.spotify.com/artist/novalima", "instagram": "https://instagram.com/novalima"},
        "audio": "https://example.com/preview/novalima.mp3",
    },
    {
        "key": "elena_tejada",
        "name": "Elena Tejada-Herrera",
        "category": "visual_art",
        "genres": ["performance", "arte contemporáneo"],
        "bio": "Artista peruana de performance y video, pionera del arte feminista en Lima.",
        "social": {"instagram": "https://instagram.com/elenatejada.art"},
        "audio": None,
    },
    {
        "key": "teatro_la_plaza",
        "name": "Teatro La Plaza",
        "category": "theater",
        "genres": ["teatro contemporáneo"],
        "bio": "Una de las compañías de teatro más influyentes de Lima.",
        "social": {"instagram": "https://instagram.com/teatrolaplaza", "website": "https://teatrolaplaza.com"},
        "audio": None,
    },
    {
        "key": "danza_viva",
        "name": "Danza Viva Perú",
        "category": "dance",
        "genres": ["danza folclórica", "marinera"],
        "bio": "Compañía dedicada a la difusión de la danza folclórica peruana.",
        "social": {"instagram": "https://instagram.com/danzavivaperu", "youtube": "https://youtube.com/@danzavivaperu"},
        "audio": None,
    },
]


# ── Events: (title, category, venue_key, [artist_keys], days_from_now, hour,
#             is_free, price, tags) ───────────────────────────────────────────
EVENTS = [
    ("Noche de Shoegaze", "music", "indie_rocks", ["lng_division", "rivera_quartet"], 3, 21, False, 280, ["indie", "envivo"]),
    ("El Mató en CDMX", "music", "indie_rocks", ["el_mato"], 12, 21, False, 650, ["indie", "rock"]),
    ("Reflejos: Instalación Lumínica", "visual_art", "galeria_omr", ["ana_torres"], 1, 11, True, None, ["arte", "instalacion"]),
    ("Cuerpos en Tránsito", "dance", "teatro_helenico", ["cia_nado"], 5, 20, False, 350, ["danza", "contemporaneo"]),
    ("Concierto de Bellas Artes: Jazz", "music", "bellas_artes", ["rivera_quartet"], 7, 19, False, 450, ["jazz", "clasico"]),
    ("Frontera: Teatro Documental", "theater", "teatro_helenico", ["teatro_linea"], 9, 20, False, 300, ["teatro", "documental"]),
    ("Ciclo de Cine de Autor", "cinema", "cineteca", [], 2, 18, False, 70, ["cine", "autor"]),
    ("Festival de la Revolución", "festival", "monumento_rev", ["lng_division", "rivera_quartet"], 15, 17, True, None, ["festival", "gratis"]),
    ("Exposición: Memoria Urbana", "visual_art", "galeria_omr", ["ana_torres"], 4, 10, True, None, ["arte", "exposicion"]),
    ("Jam Session de Jazz", "music", "indie_rocks", ["rivera_quartet"], 6, 22, False, 150, ["jazz", "jam"]),
    # ── Lima events (prices in PEN) ───────────────────────────────────────────
    ("Cumbia Amazónica en Vivo", "music", "la_noche", ["los_mirlos"], 3, 22, False, 80, ["cumbia", "envivo"]),
    ("Susana Baca: Noche Afroperuana", "music", "gran_teatro", ["susana_baca"], 8, 20, False, 120, ["afroperuano", "concierto"]),
    ("Novalima Live Set", "music", "la_noche", ["novalima"], 11, 23, False, 90, ["electronica", "fusion"]),
    ("Performance: Cuerpo y Memoria", "visual_art", "mali", ["elena_tejada"], 2, 11, True, None, ["performance", "arte"]),
    ("La Plaza: Temporada de Teatro", "theater", "teatro_municipal_lima", ["teatro_la_plaza"], 6, 20, False, 75, ["teatro", "contemporaneo"]),
    ("Gala de Marinera", "dance", "gran_teatro", ["danza_viva"], 9, 19, False, 60, ["danza", "folclor"]),
    ("Ciclo de Cine Peruano", "cinema", "cc_ricardo_palma", [], 4, 18, True, None, ["cine", "peruano"]),
    ("Festival de Música Criolla", "festival", "parque_exposicion", ["susana_baca", "novalima"], 14, 16, True, None, ["festival", "criollo"]),
    ("Exposición: Arte Colonial", "visual_art", "mali", ["elena_tejada"], 5, 10, False, 30, ["arte", "exposicion"]),
    ("Marinera y Festejo", "dance", "cc_ricardo_palma", ["danza_viva"], 7, 19, False, 50, ["danza", "marinera"]),
]


async def seed():
    async with AsyncSessionLocal() as db:
        # ── Clean slate ──────────────────────────────────────────────────────
        await db.execute(delete(EventArtist))
        await db.execute(delete(Event))
        await db.execute(delete(Artist))
        await db.execute(delete(Venue))
        await db.execute(delete(User).where(User.email == "demo@zoomartists.app"))
        await db.commit()

        # ── Organizer ────────────────────────────────────────────────────────
        organizer = User(
            email="demo@zoomartists.app",
            name="ZoomArtists Demo",
            hashed_password=hash_password("demo1234"),
            role=UserRole.organizer,
        )
        db.add(organizer)
        await db.flush()

        # ── Venues ───────────────────────────────────────────────────────────
        venues: dict[str, Venue] = {}
        for v in VENUES:
            venue = Venue(
                name=v["name"], address=v["address"], city=v["city"], country=v["country"],
                coordinates=point(v["lng"], v["lat"]),
                google_maps_url=f"https://maps.google.com/?q={v['lat']},{v['lng']}",
                capacity=v["capacity"], accessibility=v["accessibility"], transit_info=v["transit_info"],
            )
            db.add(venue)
            venues[v["key"]] = venue
        await db.flush()

        # ── Artists ──────────────────────────────────────────────────────────
        artists: dict[str, Artist] = {}
        for a in ARTISTS:
            artist = Artist(
                name=a["name"], slug=a["key"].replace("_", "-"), bio=a["bio"],
                category=a["category"], genres=a["genres"],
                profile_image=img(f"artist-{a['key']}", 400, 400),
                gallery=[img(f"{a['key']}-1"), img(f"{a['key']}-2")],
                social_links=a["social"], audio_preview_url=a["audio"],
                is_verified=True, verified_at=datetime.now(UTC),
            )
            db.add(artist)
            artists[a["key"]] = artist
        await db.flush()

        # ── Events ───────────────────────────────────────────────────────────
        now = datetime.now(UTC)
        currency_by_country = {"México": "MXN", "Perú": "PEN"}
        for title, cat, vkey, akeys, days, hour, is_free, price, tags in EVENTS:
            start = (now + timedelta(days=days)).replace(hour=hour, minute=0, second=0, microsecond=0)
            venue = venues[vkey]
            event = Event(
                title=title, description=f"{title} — un evento imperdible en {venue.name}.",
                category=EventCategory(cat), status=EventStatus.published,
                start_date=start, end_date=start + timedelta(hours=2),
                cover_image=img(f"event-{vkey}-{days}", 800, 500),
                gallery=[img(f"g-{vkey}-1"), img(f"g-{vkey}-2"), img(f"g-{vkey}-3")],
                ticket_url="https://example.com/tickets" if not is_free else None,
                ticket_price=price, currency=currency_by_country.get(venue.country, "USD"),
                is_free=is_free, capacity=venue.capacity, tags=tags,
                venue_id=venue.id, organizer_id=organizer.id,
            )
            db.add(event)
            await db.flush()
            for i, akey in enumerate(akeys):
                db.add(EventArtist(event_id=event.id, artist_id=artists[akey].id, order=i))

        await db.commit()

        print(f"Seeded: {len(VENUES)} venues, {len(ARTISTS)} artists, {len(EVENTS)} events.")
        print("Demo organizer login -> demo@zoomartists.app / demo1234")


if __name__ == "__main__":
    asyncio.run(seed())
