"""SQLAlchemy implementations of the application repository ports.

All PostGIS/SQLAlchemy specifics are confined here. Each method returns plain
domain entities (via mappers), so nothing about the database leaks past this line.
"""

from __future__ import annotations

from geoalchemy2 import Geography
from geoalchemy2.functions import (
    ST_X,
    ST_Y,
    ST_Distance,
    ST_DWithin,
    ST_GeogFromText,
    ST_GeomFromText,
)
from sqlalchemy import cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.application.dto import NearbyEvent, NearbyEventsResult, NearbyQuery
from app.application.ports import (
    ArtistRepository,
    EventRepository,
    UserRepository,
    VenueRepository,
)
from app.domain.entities import Artist, Coordinates, Event, User, Venue
from app.infrastructure.persistence.mappers import (
    artist_to_domain,
    event_to_domain,
    user_to_domain,
    venue_to_domain,
)
from app.infrastructure.persistence.models.artist import Artist as ArtistModel
from app.infrastructure.persistence.models.artist import ArtistFollow
from app.infrastructure.persistence.models.event import Event as EventModel
from app.infrastructure.persistence.models.event import (
    EventArtist,
    SavedEvent,
)
from app.infrastructure.persistence.models.event import (
    EventCategory as OrmEventCategory,
)
from app.infrastructure.persistence.models.event import (
    EventStatus as OrmEventStatus,
)
from app.infrastructure.persistence.models.user import User as UserModel
from app.infrastructure.persistence.models.user import UserRole as OrmUserRole
from app.infrastructure.persistence.models.venue import Venue as VenueModel


def _point_wkt(coords: Coordinates) -> str:
    return f"POINT({coords.longitude} {coords.latitude})"


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: str) -> User | None:
        model = await self._session.get(UserModel, user_id)
        return user_to_domain(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalar_one_or_none()
        return user_to_domain(model) if model else None

    async def add(self, user: User) -> User:
        model = UserModel(
            id=user.id,
            email=user.email,
            name=user.name,
            hashed_password=user.hashed_password,
            role=OrmUserRole(user.role.value),
            is_active=user.is_active,
            notifications_enabled=user.notifications_enabled,
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return user_to_domain(model)


class SqlAlchemyArtistRepository(ArtistRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _follower_count(self, artist_id: str) -> int:
        return (
            await self._session.execute(
                select(func.count())
                .select_from(ArtistFollow)
                .where(ArtistFollow.artist_id == artist_id)
            )
        ).scalar_one()

    async def get_by_id(self, artist_id: str) -> Artist | None:
        model = await self._session.get(ArtistModel, artist_id)
        if not model:
            return None
        return artist_to_domain(model, await self._follower_count(artist_id))

    async def get_by_slug(self, slug: str) -> Artist | None:
        result = await self._session.execute(select(ArtistModel).where(ArtistModel.slug == slug))
        model = result.scalar_one_or_none()
        return artist_to_domain(model) if model else None

    async def add(self, artist: Artist) -> Artist:
        model = ArtistModel(
            id=artist.id,
            name=artist.name,
            slug=artist.slug,
            category=artist.category,
            bio=artist.bio,
            genres=artist.genres or None,
            profile_image=artist.profile_image,
            audio_preview_url=artist.audio_preview_url,
            social_links=artist.social_links,
            user_id=artist.user_id,
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return artist_to_domain(model, 0)

    async def is_following(self, user_id: str, artist_id: str) -> bool:
        result = await self._session.execute(
            select(ArtistFollow).where(
                ArtistFollow.user_id == user_id, ArtistFollow.artist_id == artist_id
            )
        )
        return result.scalar_one_or_none() is not None

    async def add_follow(self, user_id: str, artist_id: str) -> None:
        self._session.add(ArtistFollow(user_id=user_id, artist_id=artist_id))
        await self._session.commit()

    async def remove_follow(self, user_id: str, artist_id: str) -> None:
        result = await self._session.execute(
            select(ArtistFollow).where(
                ArtistFollow.user_id == user_id, ArtistFollow.artist_id == artist_id
            )
        )
        follow = result.scalar_one_or_none()
        if follow:
            await self._session.delete(follow)
            await self._session.commit()


class SqlAlchemyVenueRepository(VenueRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, venue_id: str) -> Venue | None:
        result = await self._session.execute(
            select(VenueModel, ST_X(VenueModel.coordinates), ST_Y(VenueModel.coordinates)).where(
                VenueModel.id == venue_id
            )
        )
        row = result.one_or_none()
        if not row:
            return None
        model, lng, lat = row
        return venue_to_domain(model, Coordinates(longitude=lng, latitude=lat))

    async def add(self, venue: Venue) -> Venue:
        model = VenueModel(
            id=venue.id,
            name=venue.name,
            address=venue.address,
            city=venue.city,
            country=venue.country,
            google_maps_url=venue.google_maps_url,
            capacity=venue.capacity,
            description=venue.description,
            accessibility=venue.accessibility or None,
            transit_info=venue.transit_info or None,
            coordinates=ST_GeomFromText(_point_wkt(venue.coordinates), 4326),
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        # Coordinates are known from the command — no need to round-trip through PostGIS.
        return venue_to_domain(model, venue.coordinates)


class SqlAlchemyEventRepository(EventRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(model: EventModel, lng: float, lat: float) -> Event:
        venue = venue_to_domain(model.venue, Coordinates(longitude=lng, latitude=lat))
        artists = [
            artist_to_domain(ea.artist)
            for ea in sorted(model.event_artists, key=lambda x: x.order)
        ]
        return event_to_domain(model, venue, artists)

    async def get_by_id(self, event_id: str, *, include_hidden: bool = False) -> Event | None:
        query = (
            select(EventModel, ST_X(VenueModel.coordinates), ST_Y(VenueModel.coordinates))
            .join(VenueModel, EventModel.venue_id == VenueModel.id)
            .options(
                selectinload(EventModel.venue),
                selectinload(EventModel.event_artists).selectinload(EventArtist.artist),
            )
            .where(EventModel.id == event_id)
        )
        if not include_hidden:
            query = query.where(EventModel.status != OrmEventStatus.draft)

        row = (await self._session.execute(query)).one_or_none()
        if not row:
            return None
        model, lng, lat = row
        return self._to_domain(model, lng, lat)

    async def find_nearby(self, query: NearbyQuery) -> NearbyEventsResult:
        user_point = ST_GeogFromText(
            _point_wkt(Coordinates(longitude=query.longitude, latitude=query.latitude))
        )
        distance = ST_Distance(cast(VenueModel.coordinates, Geography), user_point).label(
            "distance_meters"
        )
        venue_geog = cast(VenueModel.coordinates, Geography)
        within = ST_DWithin(venue_geog, user_point, query.radius_meters)

        stmt = (
            select(distance, ST_X(VenueModel.coordinates), ST_Y(VenueModel.coordinates), EventModel)
            .join(VenueModel, EventModel.venue_id == VenueModel.id)
            .options(
                selectinload(EventModel.venue),
                selectinload(EventModel.event_artists).selectinload(EventArtist.artist),
            )
            .where(EventModel.status == OrmEventStatus.published, within)
            .order_by(distance)
            .limit(query.limit)
        )
        count_stmt = (
            select(func.count())
            .select_from(EventModel)
            .join(VenueModel, EventModel.venue_id == VenueModel.id)
            .where(EventModel.status == OrmEventStatus.published, within)
        )
        if query.category:
            cat = OrmEventCategory(query.category.value)
            stmt = stmt.where(EventModel.category == cat)
            count_stmt = count_stmt.where(EventModel.category == cat)
        if query.is_free is not None:
            stmt = stmt.where(EventModel.is_free == query.is_free)
            count_stmt = count_stmt.where(EventModel.is_free == query.is_free)

        rows = (await self._session.execute(stmt)).all()
        total = (await self._session.execute(count_stmt)).scalar_one()

        events = [
            NearbyEvent(
                event=self._to_domain(model, lng, lat),
                distance_meters=round(dist, 1) if dist is not None else None,
            )
            for dist, lng, lat, model in rows
        ]
        return NearbyEventsResult(events=events, total=total)

    async def add(self, event: Event, artist_ids: list[str]) -> Event:
        model = EventModel(
            id=event.id,
            title=event.title,
            description=event.description,
            category=OrmEventCategory(event.category.value),
            status=OrmEventStatus(event.status.value),
            start_date=event.start_date,
            end_date=event.end_date,
            video_url=event.video_url,
            ticket_url=event.ticket_url,
            ticket_price=event.ticket_price,
            currency=event.currency,
            is_free=event.is_free,
            capacity=event.capacity,
            tags=event.tags or None,
            venue_id=event.venue.id,
            organizer_id=event.organizer_id,
        )
        self._session.add(model)
        await self._session.flush()
        for i, artist_id in enumerate(artist_ids):
            self._session.add(EventArtist(event_id=model.id, artist_id=artist_id, order=i))
        await self._session.commit()
        return await self.get_by_id(model.id, include_hidden=True)

    async def update(self, event_id: str, changes: dict) -> Event:
        model = await self._session.get(EventModel, event_id)
        for field, value in changes.items():
            if field == "category":
                value = OrmEventCategory(value.value)
            elif field == "status":
                value = OrmEventStatus(value.value)
            setattr(model, field, value)
        await self._session.commit()
        return await self.get_by_id(event_id, include_hidden=True)

    async def delete(self, event_id: str) -> None:
        model = await self._session.get(EventModel, event_id)
        if model:
            await self._session.delete(model)
            await self._session.commit()

    async def is_saved(self, user_id: str, event_id: str) -> bool:
        result = await self._session.execute(
            select(SavedEvent).where(
                SavedEvent.user_id == user_id, SavedEvent.event_id == event_id
            )
        )
        return result.scalar_one_or_none() is not None

    async def save_for_user(self, user_id: str, event_id: str) -> None:
        self._session.add(SavedEvent(user_id=user_id, event_id=event_id))
        await self._session.commit()

    async def unsave_for_user(self, user_id: str, event_id: str) -> None:
        result = await self._session.execute(
            select(SavedEvent).where(
                SavedEvent.user_id == user_id, SavedEvent.event_id == event_id
            )
        )
        saved = result.scalar_one_or_none()
        if saved:
            await self._session.delete(saved)
            await self._session.commit()
