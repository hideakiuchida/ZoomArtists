from fastapi import APIRouter, Depends, status

from app.api.deps import get_venue_repository, require_role
from app.api.schemas.venue import VenueCreate, VenueResponse
from app.application.dto import CreateVenueCommand
from app.application.ports import VenueRepository
from app.application.venues import CreateVenue, GetVenue, ListVenues
from app.domain.entities import UserRole

router = APIRouter(prefix="/venues", tags=["venues"])


@router.get("", response_model=list[VenueResponse])
async def list_venues(
    _=Depends(require_role(UserRole.organizer, UserRole.admin, UserRole.artist)),
    venues: VenueRepository = Depends(get_venue_repository),
):
    result = await ListVenues(venues).execute()
    return [VenueResponse.from_entity(v) for v in result]


@router.post("", response_model=VenueResponse, status_code=status.HTTP_201_CREATED)
async def create_venue(
    body: VenueCreate,
    _=Depends(require_role(UserRole.organizer, UserRole.admin)),
    venues: VenueRepository = Depends(get_venue_repository),
):
    cmd = CreateVenueCommand(
        name=body.name,
        address=body.address,
        city=body.city,
        country=body.country,
        coordinates=body.coordinates.to_entity(),
        google_maps_url=str(body.google_maps_url) if body.google_maps_url else None,
        capacity=body.capacity,
        description=body.description,
        accessibility=body.accessibility,
        transit_info=body.transit_info,
    )
    venue = await CreateVenue(venues).execute(cmd)
    return VenueResponse.from_entity(venue)


@router.get("/{venue_id}", response_model=VenueResponse)
async def get_venue(
    venue_id: str,
    venues: VenueRepository = Depends(get_venue_repository),
):
    venue = await GetVenue(venues).execute(venue_id)
    return VenueResponse.from_entity(venue)
