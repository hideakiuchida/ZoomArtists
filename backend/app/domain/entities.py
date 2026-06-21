"""Domain entities and value objects.

Plain dataclasses encapsulating enterprise-wide business rules. They are *not*
database rows and carry no persistence or serialization concerns — the ORM lives
in infrastructure, the wire DTOs live in the api layer. Critical rules that would
hold true regardless of delivery mechanism live here as methods.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime


class UserRole(str, enum.Enum):
    attendee = "attendee"
    artist = "artist"
    organizer = "organizer"
    admin = "admin"


class EventCategory(str, enum.Enum):
    music = "music"
    visual_art = "visual_art"
    theater = "theater"
    dance = "dance"
    spoken_word = "spoken_word"
    cinema = "cinema"
    festival = "festival"
    workshop = "workshop"
    street_performance = "street_performance"


class EventStatus(str, enum.Enum):
    draft = "draft"
    pending = "pending"
    published = "published"
    cancelled = "cancelled"
    past = "past"


@dataclass
class Coordinates:
    """A geographic point. Longitude/latitude, WGS84."""

    longitude: float
    latitude: float


@dataclass
class User:
    id: str
    email: str
    name: str
    role: UserRole = UserRole.attendee
    is_active: bool = True
    notifications_enabled: bool = True
    avatar: str | None = None
    hashed_password: str | None = None
    pref_lat: float | None = None
    pref_lng: float | None = None
    pref_radius_km: int = 5
    saved_event_ids: list[str] = field(default_factory=list)
    followed_artist_ids: list[str] = field(default_factory=list)

    def has_any_role(self, *roles: UserRole) -> bool:
        return self.role in roles

    def can_manage_event(self, organizer_id: str) -> bool:
        """An event may be managed by its organizer or by an admin."""
        return self.id == organizer_id or self.role == UserRole.admin

    @property
    def location_preference(self) -> Coordinates | None:
        if self.pref_lat is None or self.pref_lng is None:
            return None
        return Coordinates(longitude=self.pref_lng, latitude=self.pref_lat)


@dataclass
class Artist:
    id: str
    name: str
    slug: str
    category: str
    bio: str | None = None
    genres: list[str] = field(default_factory=list)
    profile_image: str | None = None
    gallery: list[str] = field(default_factory=list)
    audio_preview_url: str | None = None
    social_links: dict | None = None
    is_verified: bool = False
    verified_at: datetime | None = None
    user_id: str | None = None
    follower_count: int = 0


@dataclass
class Venue:
    id: str
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


@dataclass
class Event:
    id: str
    title: str
    category: EventCategory
    status: EventStatus
    start_date: datetime
    venue: Venue
    organizer_id: str
    description: str | None = None
    end_date: datetime | None = None
    cover_image: str | None = None
    gallery: list[str] = field(default_factory=list)
    video_url: str | None = None
    ticket_url: str | None = None
    ticket_price: float | None = None
    currency: str = "MXN"
    is_free: bool = False
    capacity: int | None = None
    tags: list[str] = field(default_factory=list)
    artists: list[Artist] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def is_visible(self) -> bool:
        """Drafts are never shown through public read endpoints."""
        return self.status != EventStatus.draft
