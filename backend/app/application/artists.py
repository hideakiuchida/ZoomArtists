"""Artist use cases."""

from __future__ import annotations

from uuid import uuid4

from app.application.dto import CreateArtistCommand
from app.application.ports import ArtistRepository
from app.domain.entities import Artist, User
from app.domain.errors import ConflictError, NotFoundError


class GetArtist:
    def __init__(self, artists: ArtistRepository) -> None:
        self._artists = artists

    async def execute(self, artist_id: str) -> Artist:
        artist = await self._artists.get_by_id(artist_id)
        if not artist:
            raise NotFoundError("Artist not found")
        return artist


class CreateArtist:
    def __init__(self, artists: ArtistRepository) -> None:
        self._artists = artists

    async def execute(self, cmd: CreateArtistCommand, actor: User) -> Artist:
        if await self._artists.get_by_slug(cmd.slug):
            raise ConflictError("Slug already taken")

        artist = Artist(
            id=str(uuid4()),
            name=cmd.name,
            slug=cmd.slug,
            category=cmd.category,
            bio=cmd.bio,
            genres=cmd.genres,
            profile_image=cmd.profile_image,
            audio_preview_url=cmd.audio_preview_url,
            social_links=cmd.social_links or None,
            user_id=actor.id,
        )
        return await self._artists.add(artist)


class FollowArtist:
    def __init__(self, artists: ArtistRepository) -> None:
        self._artists = artists

    async def execute(self, artist_id: str, actor: User) -> None:
        if not await self._artists.get_by_id(artist_id):
            raise NotFoundError("Artist not found")
        if not await self._artists.is_following(actor.id, artist_id):
            await self._artists.add_follow(actor.id, artist_id)


class UnfollowArtist:
    def __init__(self, artists: ArtistRepository) -> None:
        self._artists = artists

    async def execute(self, artist_id: str, actor: User) -> None:
        await self._artists.remove_follow(actor.id, artist_id)
