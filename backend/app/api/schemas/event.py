from datetime import datetime

from pydantic import BaseModel, HttpUrl

from app.api.schemas.artist import ArtistSummary
from app.api.schemas.venue import Coordinates, VenueResponse
from app.application.dto import NearbyEvent, NearbyEventsResult
from app.domain.entities import Event, EventCategory, EventStatus


class EventCreate(BaseModel):
    title: str
    description: str | None = None
    category: EventCategory
    start_date: datetime
    end_date: datetime | None = None
    venue_id: str
    artist_ids: list[str] = []
    ticket_url: HttpUrl | None = None
    ticket_price: float | None = None
    currency: str = "MXN"
    is_free: bool = False
    capacity: int | None = None
    tags: list[str] = []
    video_url: str | None = None


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: EventCategory | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    ticket_url: HttpUrl | None = None
    ticket_price: float | None = None
    is_free: bool | None = None
    capacity: int | None = None
    tags: list[str] | None = None
    status: EventStatus | None = None


class EventSummary(BaseModel):
    id: str
    title: str
    category: EventCategory
    status: EventStatus
    start_date: datetime
    cover_image: str | None = None
    is_free: bool
    ticket_price: float | None = None
    currency: str
    coordinates: Coordinates
    distance_meters: float | None = None
    venue_name: str
    artist_names: list[str] = []

    @classmethod
    def from_nearby(cls, item: NearbyEvent) -> "EventSummary":
        event = item.event
        return cls(
            id=event.id,
            title=event.title,
            category=event.category,
            status=event.status,
            start_date=event.start_date,
            cover_image=event.cover_image,
            is_free=event.is_free,
            ticket_price=event.ticket_price,
            currency=event.currency,
            coordinates=Coordinates(
                longitude=event.venue.coordinates.longitude,
                latitude=event.venue.coordinates.latitude,
            ),
            distance_meters=item.distance_meters,
            venue_name=event.venue.name,
            artist_names=[a.name for a in event.artists],
        )


class EventResponse(BaseModel):
    id: str
    title: str
    description: str | None = None
    category: EventCategory
    status: EventStatus
    start_date: datetime
    end_date: datetime | None = None
    cover_image: str | None = None
    gallery: list[str] = []
    video_url: str | None = None
    ticket_url: str | None = None
    ticket_price: float | None = None
    currency: str
    is_free: bool
    capacity: int | None = None
    tags: list[str] = []
    coordinates: Coordinates
    distance_meters: float | None = None
    venue: VenueResponse
    artists: list[ArtistSummary] = []
    organizer_id: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, event: Event) -> "EventResponse":
        coords = Coordinates(
            longitude=event.venue.coordinates.longitude,
            latitude=event.venue.coordinates.latitude,
        )
        return cls(
            id=event.id,
            title=event.title,
            description=event.description,
            category=event.category,
            status=event.status,
            start_date=event.start_date,
            end_date=event.end_date,
            cover_image=event.cover_image,
            gallery=event.gallery,
            video_url=event.video_url,
            ticket_url=event.ticket_url,
            ticket_price=event.ticket_price,
            currency=event.currency,
            is_free=event.is_free,
            capacity=event.capacity,
            tags=event.tags,
            coordinates=coords,
            distance_meters=None,
            venue=VenueResponse.from_entity(event.venue),
            artists=[ArtistSummary.from_entity(a) for a in event.artists],
            organizer_id=event.organizer_id,
            created_at=event.created_at,
            updated_at=event.updated_at,
        )


class NearbyEventsResponse(BaseModel):
    events: list[EventSummary]
    total: int
    next_cursor: str | None = None

    @classmethod
    def from_result(cls, result: NearbyEventsResult) -> "NearbyEventsResponse":
        return cls(
            events=[EventSummary.from_nearby(item) for item in result.events],
            total=result.total,
        )
