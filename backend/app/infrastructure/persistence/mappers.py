"""Translation between ORM rows and domain entities.

Keeps SQLAlchemy types from leaking inward: the application and domain layers only
ever see plain domain entities. Coordinates are passed in explicitly because they
must be extracted from the PostGIS geometry with ST_X/ST_Y at query time.
"""

from __future__ import annotations

from app.domain.entities import (
    Artist,
    Coordinates,
    Event,
    EventCategory,
    EventStatus,
    User,
    UserRole,
    Venue,
)
from app.infrastructure.persistence.models.artist import Artist as ArtistModel
from app.infrastructure.persistence.models.event import Event as EventModel
from app.infrastructure.persistence.models.user import User as UserModel
from app.infrastructure.persistence.models.venue import Venue as VenueModel


def user_to_domain(
    m: UserModel,
    *,
    saved_event_ids: list[str] | None = None,
    followed_artist_ids: list[str] | None = None,
) -> User:
    # Collection ids are passed in explicitly by the repository when needed, so we
    # never trip an async lazy-load on relationships that weren't eagerly fetched.
    return User(
        id=m.id,
        email=m.email,
        name=m.name,
        role=UserRole(m.role.value),
        is_active=m.is_active,
        notifications_enabled=m.notifications_enabled,
        avatar=m.avatar,
        hashed_password=m.hashed_password,
        pref_lat=m.pref_lat,
        pref_lng=m.pref_lng,
        pref_radius_km=m.pref_radius_km,
        saved_event_ids=saved_event_ids or [],
        followed_artist_ids=followed_artist_ids or [],
    )


def artist_to_domain(m: ArtistModel, follower_count: int = 0) -> Artist:
    return Artist(
        id=m.id,
        name=m.name,
        slug=m.slug,
        category=m.category,
        bio=m.bio,
        genres=m.genres or [],
        profile_image=m.profile_image,
        gallery=m.gallery or [],
        audio_preview_url=m.audio_preview_url,
        social_links=m.social_links,
        is_verified=m.is_verified,
        verified_at=m.verified_at,
        user_id=m.user_id,
        follower_count=follower_count,
    )


def venue_to_domain(m: VenueModel, coordinates: Coordinates) -> Venue:
    return Venue(
        id=m.id,
        name=m.name,
        address=m.address,
        city=m.city,
        country=m.country,
        coordinates=coordinates,
        google_maps_url=m.google_maps_url,
        capacity=m.capacity,
        description=m.description,
        accessibility=m.accessibility or [],
        transit_info=m.transit_info or [],
    )


def event_to_domain(m: EventModel, venue: Venue, artists: list[Artist]) -> Event:
    return Event(
        id=m.id,
        title=m.title,
        category=EventCategory(m.category.value),
        status=EventStatus(m.status.value),
        start_date=m.start_date,
        venue=venue,
        organizer_id=m.organizer_id,
        description=m.description,
        end_date=m.end_date,
        cover_image=m.cover_image,
        gallery=m.gallery or [],
        video_url=m.video_url,
        ticket_url=m.ticket_url,
        ticket_price=m.ticket_price,
        currency=m.currency,
        is_free=m.is_free,
        capacity=m.capacity,
        tags=m.tags or [],
        artists=artists,
        created_at=m.created_at,
        updated_at=m.updated_at,
    )
