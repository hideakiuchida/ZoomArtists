from pydantic import BaseModel, HttpUrl

from app.domain.entities import Coordinates as CoordinatesEntity
from app.domain.entities import Venue


class Coordinates(BaseModel):
    longitude: float
    latitude: float

    def to_entity(self) -> CoordinatesEntity:
        return CoordinatesEntity(longitude=self.longitude, latitude=self.latitude)


class VenueCreate(BaseModel):
    name: str
    address: str
    city: str
    country: str
    coordinates: Coordinates
    google_maps_url: HttpUrl | None = None
    capacity: int | None = None
    description: str | None = None
    accessibility: list[str] = []
    transit_info: list[str] = []


class VenueResponse(BaseModel):
    id: str
    name: str
    address: str
    city: str
    country: str
    coordinates: Coordinates
    google_maps_url: str | None = None
    capacity: int | None = None
    description: str | None = None
    accessibility: list[str] = []
    transit_info: list[str] = []

    @classmethod
    def from_entity(cls, venue: Venue) -> "VenueResponse":
        return cls(
            id=venue.id,
            name=venue.name,
            address=venue.address,
            city=venue.city,
            country=venue.country,
            coordinates=Coordinates(
                longitude=venue.coordinates.longitude, latitude=venue.coordinates.latitude
            ),
            google_maps_url=venue.google_maps_url,
            capacity=venue.capacity,
            description=venue.description,
            accessibility=venue.accessibility,
            transit_info=venue.transit_info,
        )
