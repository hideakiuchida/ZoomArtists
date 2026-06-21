from fastapi import APIRouter, Depends, Query, status

from app.api.deps import (
    get_current_user,
    get_event_repository,
    get_venue_repository,
    require_role,
)
from app.api.schemas.event import (
    EventCreate,
    EventResponse,
    EventUpdate,
    NearbyEventsResponse,
)
from app.application.dto import CreateEventCommand, NearbyQuery, UpdateEventCommand
from app.application.events import (
    CreateEvent,
    DeleteEvent,
    GetEvent,
    GetNearbyEvents,
    SaveEvent,
    UnsaveEvent,
    UpdateEvent,
)
from app.application.ports import EventRepository, VenueRepository
from app.domain.entities import EventCategory, User, UserRole

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/nearby", response_model=NearbyEventsResponse)
async def get_nearby_events(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    radius: int = Query(5000, ge=100, le=100_000, description="Radius in meters"),
    category: EventCategory | None = None,
    is_free: bool | None = None,
    limit: int = Query(50, ge=1, le=100),
    events: EventRepository = Depends(get_event_repository),
):
    result = await GetNearbyEvents(events).execute(
        NearbyQuery(
            latitude=lat,
            longitude=lng,
            radius_meters=radius,
            category=category,
            is_free=is_free,
            limit=limit,
        )
    )
    return NearbyEventsResponse.from_result(result)


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: str,
    events: EventRepository = Depends(get_event_repository),
):
    event = await GetEvent(events).execute(event_id)
    return EventResponse.from_entity(event)


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    body: EventCreate,
    current_user: User = Depends(
        require_role(UserRole.organizer, UserRole.admin, UserRole.artist)
    ),
    events: EventRepository = Depends(get_event_repository),
    venues: VenueRepository = Depends(get_venue_repository),
):
    cmd = CreateEventCommand(
        title=body.title,
        category=body.category,
        start_date=body.start_date,
        venue_id=body.venue_id,
        description=body.description,
        end_date=body.end_date,
        artist_ids=body.artist_ids,
        ticket_url=str(body.ticket_url) if body.ticket_url else None,
        ticket_price=body.ticket_price,
        currency=body.currency,
        is_free=body.is_free,
        capacity=body.capacity,
        tags=body.tags,
        video_url=body.video_url,
    )
    event = await CreateEvent(events, venues).execute(cmd, current_user)
    return EventResponse.from_entity(event)


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: str,
    body: EventUpdate,
    current_user: User = Depends(get_current_user),
    events: EventRepository = Depends(get_event_repository),
):
    cmd = UpdateEventCommand(
        title=body.title,
        description=body.description,
        category=body.category,
        start_date=body.start_date,
        end_date=body.end_date,
        ticket_url=str(body.ticket_url) if body.ticket_url else None,
        ticket_price=body.ticket_price,
        is_free=body.is_free,
        capacity=body.capacity,
        tags=body.tags,
        status=body.status,
    )
    event = await UpdateEvent(events).execute(event_id, cmd, current_user)
    return EventResponse.from_entity(event)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: str,
    current_user: User = Depends(get_current_user),
    events: EventRepository = Depends(get_event_repository),
):
    await DeleteEvent(events).execute(event_id, current_user)


@router.post("/{event_id}/save", status_code=status.HTTP_204_NO_CONTENT)
async def save_event(
    event_id: str,
    current_user: User = Depends(get_current_user),
    events: EventRepository = Depends(get_event_repository),
):
    await SaveEvent(events).execute(event_id, current_user)


@router.delete("/{event_id}/save", status_code=status.HTTP_204_NO_CONTENT)
async def unsave_event(
    event_id: str,
    current_user: User = Depends(get_current_user),
    events: EventRepository = Depends(get_event_repository),
):
    await UnsaveEvent(events).execute(event_id, current_user)
