"""Venue use cases."""

from __future__ import annotations

from uuid import uuid4

from app.application.dto import CreateVenueCommand
from app.application.ports import VenueRepository
from app.domain.entities import Venue
from app.domain.errors import NotFoundError


class GetVenue:
    def __init__(self, venues: VenueRepository) -> None:
        self._venues = venues

    async def execute(self, venue_id: str) -> Venue:
        venue = await self._venues.get_by_id(venue_id)
        if not venue:
            raise NotFoundError("Venue not found")
        return venue


class ListVenues:
    def __init__(self, venues: VenueRepository) -> None:
        self._venues = venues

    async def execute(self) -> list[Venue]:
        return await self._venues.list_all()


class CreateVenue:
    def __init__(self, venues: VenueRepository) -> None:
        self._venues = venues

    async def execute(self, cmd: CreateVenueCommand) -> Venue:
        venue = Venue(
            id=str(uuid4()),
            name=cmd.name,
            address=cmd.address,
            city=cmd.city,
            country=cmd.country,
            coordinates=cmd.coordinates,
            google_maps_url=cmd.google_maps_url,
            capacity=cmd.capacity,
            description=cmd.description,
            accessibility=cmd.accessibility,
            transit_info=cmd.transit_info,
        )
        return await self._venues.add(venue)
