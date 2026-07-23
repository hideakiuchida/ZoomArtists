"""SQLAlchemy ORM models — a persistence detail, confined to infrastructure.

Importing this package registers every table on ``Base.metadata`` (used by Alembic
autogenerate and the seed script).
"""

from app.infrastructure.persistence.models.artist import Artist, ArtistFollow
from app.infrastructure.persistence.models.event import (
    Event,
    EventArtist,
    EventCategory,
    EventStatus,
    SavedEvent,
)
from app.infrastructure.persistence.models.user import User, UserRole
from app.infrastructure.persistence.models.venue import Venue

__all__ = [
    "User",
    "UserRole",
    "Venue",
    "Artist",
    "ArtistFollow",
    "Event",
    "EventArtist",
    "EventCategory",
    "EventStatus",
    "SavedEvent",
]
