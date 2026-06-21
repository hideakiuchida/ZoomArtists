"""Ports — abstract interfaces the use cases depend on.

These contracts are *defined inward* (by the application, in terms of domain
entities) and *implemented outward* (by infrastructure adapters). This is the
Dependency Inversion mechanism that lets us swap the database, hashing scheme, or
token format without touching a single use case.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.dto import NearbyEventsResult, NearbyQuery
from app.domain.entities import Artist, Event, User, Venue


# ── Repository ports ─────────────────────────────────────────────────────────
class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def add(self, user: User) -> User: ...


class ArtistRepository(ABC):
    @abstractmethod
    async def get_by_id(self, artist_id: str) -> Artist | None: ...

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Artist | None: ...

    @abstractmethod
    async def add(self, artist: Artist) -> Artist: ...

    @abstractmethod
    async def is_following(self, user_id: str, artist_id: str) -> bool: ...

    @abstractmethod
    async def add_follow(self, user_id: str, artist_id: str) -> None: ...

    @abstractmethod
    async def remove_follow(self, user_id: str, artist_id: str) -> None: ...


class VenueRepository(ABC):
    @abstractmethod
    async def get_by_id(self, venue_id: str) -> Venue | None: ...

    @abstractmethod
    async def add(self, venue: Venue) -> Venue: ...


class EventRepository(ABC):
    @abstractmethod
    async def get_by_id(self, event_id: str, *, include_hidden: bool = False) -> Event | None: ...

    @abstractmethod
    async def find_nearby(self, query: NearbyQuery) -> NearbyEventsResult: ...

    @abstractmethod
    async def add(self, event: Event, artist_ids: list[str]) -> Event: ...

    @abstractmethod
    async def update(self, event_id: str, changes: dict) -> Event: ...

    @abstractmethod
    async def delete(self, event_id: str) -> None: ...

    @abstractmethod
    async def is_saved(self, user_id: str, event_id: str) -> bool: ...

    @abstractmethod
    async def save_for_user(self, user_id: str, event_id: str) -> None: ...

    @abstractmethod
    async def unsave_for_user(self, user_id: str, event_id: str) -> None: ...


# ── Service ports ────────────────────────────────────────────────────────────
class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str: ...

    @abstractmethod
    def verify(self, plain: str, hashed: str) -> bool: ...


class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, subject: str) -> str: ...

    @abstractmethod
    def create_refresh_token(self, subject: str) -> str: ...

    @abstractmethod
    def decode(self, token: str) -> str | None: ...
