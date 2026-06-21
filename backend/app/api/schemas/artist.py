from datetime import datetime

from pydantic import BaseModel, HttpUrl

from app.domain.entities import Artist


class SocialLinks(BaseModel):
    instagram: HttpUrl | None = None
    spotify: HttpUrl | None = None
    soundcloud: HttpUrl | None = None
    youtube: HttpUrl | None = None
    website: HttpUrl | None = None


class ArtistCreate(BaseModel):
    name: str
    slug: str
    bio: str | None = None
    category: str
    genres: list[str] = []
    profile_image: str | None = None
    audio_preview_url: str | None = None
    social_links: SocialLinks = SocialLinks()


class ArtistSummary(BaseModel):
    id: str
    name: str
    profile_image: str | None = None
    genres: list[str] = []
    category: str

    @classmethod
    def from_entity(cls, artist: Artist) -> "ArtistSummary":
        return cls(
            id=artist.id,
            name=artist.name,
            profile_image=artist.profile_image,
            genres=artist.genres,
            category=artist.category,
        )


class ArtistResponse(BaseModel):
    id: str
    name: str
    slug: str
    bio: str | None = None
    category: str
    genres: list[str] = []
    profile_image: str | None = None
    gallery: list[str] = []
    audio_preview_url: str | None = None
    social_links: dict | None = None
    is_verified: bool = False
    verified_at: datetime | None = None
    follower_count: int = 0

    @classmethod
    def from_entity(cls, artist: Artist) -> "ArtistResponse":
        return cls(
            id=artist.id,
            name=artist.name,
            slug=artist.slug,
            bio=artist.bio,
            category=artist.category,
            genres=artist.genres,
            profile_image=artist.profile_image,
            gallery=artist.gallery,
            audio_preview_url=artist.audio_preview_url,
            social_links=artist.social_links,
            is_verified=artist.is_verified,
            verified_at=artist.verified_at,
            follower_count=artist.follower_count,
        )
