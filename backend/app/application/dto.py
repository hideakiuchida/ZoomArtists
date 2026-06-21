"""Command and result DTOs that cross the use-case boundary.

Plain dataclasses in the form most convenient for the inner circle. Controllers
translate HTTP requests into commands; use cases return entities or these result
objects. No Pydantic, no HTTP, no ORM types appear here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.entities import Coordinates, Event, EventCategory, EventStatus


# ── Auth ──────────────────────────────────────────────────────────────────────
@dataclass
class RegisterCommand:
    email: str
    name: str
    password: str


@dataclass
class LoginCommand:
    email: str
    password: str


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str


# ── Artists ───────────────────────────────────────────────────────────────────
@dataclass
class CreateArtistCommand:
    name: str
    slug: str
    category: str
    bio: str | None = None
    genres: list[str] = field(default_factory=list)
    profile_image: str | None = None
    audio_preview_url: str | None = None
    social_links: dict = field(default_factory=dict)


# ── Venues ────────────────────────────────────────────────────────────────────
@dataclass
class CreateVenueCommand:
    name: str
    address: str
    city: str
    country: str
    coordinates: Coordinates
    google_maps_url: str | None = None
    capacity: int | None = None
    description: str | None = None
    accessibility: list[str] = field(default_factory=list)
    transit_info: list[str] = field(default_factory=list)


# ── Events ────────────────────────────────────────────────────────────────────
@dataclass
class CreateEventCommand:
    title: str
    category: EventCategory
    start_date: datetime
    venue_id: str
    description: str | None = None
    end_date: datetime | None = None
    artist_ids: list[str] = field(default_factory=list)
    ticket_url: str | None = None
    ticket_price: float | None = None
    currency: str = "MXN"
    is_free: bool = False
    capacity: int | None = None
    tags: list[str] = field(default_factory=list)
    video_url: str | None = None


@dataclass
class UpdateEventCommand:
    """Only fields explicitly provided (non-None) are applied."""

    title: str | None = None
    description: str | None = None
    category: EventCategory | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    ticket_url: str | None = None
    ticket_price: float | None = None
    is_free: bool | None = None
    capacity: int | None = None
    tags: list[str] | None = None
    status: EventStatus | None = None

    def changes(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class NearbyQuery:
    latitude: float
    longitude: float
    radius_meters: int = 5000
    category: EventCategory | None = None
    is_free: bool | None = None
    limit: int = 50


@dataclass
class NearbyEvent:
    event: Event
    distance_meters: float | None


@dataclass
class NearbyEventsResult:
    events: list[NearbyEvent]
    total: int
