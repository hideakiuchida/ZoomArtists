"""Event use cases."""

from __future__ import annotations

from uuid import uuid4

from app.application.dto import (
    CreateEventCommand,
    NearbyEventsResult,
    NearbyQuery,
    UpdateEventCommand,
)
from app.application.ports import EventRepository, VenueRepository
from app.domain.entities import Event, EventStatus, User
from app.domain.errors import NotFoundError, PermissionDeniedError


class GetNearbyEvents:
    def __init__(self, events: EventRepository) -> None:
        self._events = events

    async def execute(self, query: NearbyQuery) -> NearbyEventsResult:
        return await self._events.find_nearby(query)


class GetEvent:
    def __init__(self, events: EventRepository) -> None:
        self._events = events

    async def execute(self, event_id: str) -> Event:
        event = await self._events.get_by_id(event_id)
        if not event:
            raise NotFoundError("Event not found")
        return event


class CreateEvent:
    def __init__(self, events: EventRepository, venues: VenueRepository) -> None:
        self._events = events
        self._venues = venues

    async def execute(self, cmd: CreateEventCommand, actor: User) -> Event:
        venue = await self._venues.get_by_id(cmd.venue_id)
        if not venue:
            raise NotFoundError("Venue not found")

        event = Event(
            id=str(uuid4()),
            title=cmd.title,
            category=cmd.category,
            status=EventStatus.pending,
            start_date=cmd.start_date,
            venue=venue,
            organizer_id=actor.id,
            description=cmd.description,
            end_date=cmd.end_date,
            video_url=cmd.video_url,
            ticket_url=cmd.ticket_url,
            ticket_price=cmd.ticket_price,
            currency=cmd.currency,
            is_free=cmd.is_free,
            capacity=cmd.capacity,
            tags=cmd.tags,
        )
        return await self._events.add(event, cmd.artist_ids)


class UpdateEvent:
    def __init__(self, events: EventRepository) -> None:
        self._events = events

    async def execute(self, event_id: str, cmd: UpdateEventCommand, actor: User) -> Event:
        event = await self._events.get_by_id(event_id, include_hidden=True)
        if not event:
            raise NotFoundError("Event not found")
        if not actor.can_manage_event(event.organizer_id):
            raise PermissionDeniedError("Not authorized")
        return await self._events.update(event_id, cmd.changes())


class DeleteEvent:
    def __init__(self, events: EventRepository) -> None:
        self._events = events

    async def execute(self, event_id: str, actor: User) -> None:
        event = await self._events.get_by_id(event_id, include_hidden=True)
        if not event:
            raise NotFoundError("Event not found")
        if not actor.can_manage_event(event.organizer_id):
            raise PermissionDeniedError("Not authorized")
        await self._events.delete(event_id)


class SaveEvent:
    def __init__(self, events: EventRepository) -> None:
        self._events = events

    async def execute(self, event_id: str, actor: User) -> None:
        if not await self._events.is_saved(actor.id, event_id):
            await self._events.save_for_user(actor.id, event_id)


class UnsaveEvent:
    def __init__(self, events: EventRepository) -> None:
        self._events = events

    async def execute(self, event_id: str, actor: User) -> None:
        await self._events.unsave_for_user(actor.id, event_id)
