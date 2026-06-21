from pydantic import BaseModel, EmailStr

from app.api.schemas.venue import Coordinates
from app.domain.entities import User, UserRole


class LocationPreferences(BaseModel):
    default_coordinates: Coordinates
    default_radius_km: int = 5


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    avatar: str | None = None
    role: UserRole
    notifications_enabled: bool
    location_preferences: LocationPreferences | None = None
    saved_event_ids: list[str] = []
    followed_artist_ids: list[str] = []

    @classmethod
    def from_entity(cls, user: User) -> "UserResponse":
        prefs = None
        if user.location_preference is not None:
            prefs = LocationPreferences(
                default_coordinates=Coordinates(
                    longitude=user.location_preference.longitude,
                    latitude=user.location_preference.latitude,
                ),
                default_radius_km=user.pref_radius_km,
            )
        return cls(
            id=user.id,
            email=user.email,
            name=user.name,
            avatar=user.avatar,
            role=user.role,
            notifications_enabled=user.notifications_enabled,
            location_preferences=prefs,
            saved_event_ids=user.saved_event_ids,
            followed_artist_ids=user.followed_artist_ids,
        )


class UserUpdate(BaseModel):
    name: str | None = None
    avatar: str | None = None
    notifications_enabled: bool | None = None
    location_preferences: LocationPreferences | None = None
