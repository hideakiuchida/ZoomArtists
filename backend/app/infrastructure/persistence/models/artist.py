from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.database import Base
from app.infrastructure.persistence.models.base import TimestampMixin, UUIDMixin


class Artist(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "artists"

    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String, nullable=False)
    genres: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    profile_image: Mapped[str | None] = mapped_column(String, nullable=True)
    gallery: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    audio_preview_url: Mapped[str | None] = mapped_column(String, nullable=True)
    # {"instagram": "...", "spotify": "...", "youtube": "...", ...}
    social_links: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verified_at: Mapped[object | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Link to user account (optional)
    user_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    event_artists: Mapped[list["EventArtist"]] = relationship(  # noqa: F821
        "EventArtist", back_populates="artist"
    )
    followers: Mapped[list["ArtistFollow"]] = relationship(  # noqa: F821
        "ArtistFollow", back_populates="artist"
    )


class ArtistFollow(Base, UUIDMixin):
    __tablename__ = "artist_follows"

    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"))
    artist_id: Mapped[str] = mapped_column(String, ForeignKey("artists.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship("User", back_populates="followed_artists")  # noqa: F821
    artist: Mapped[Artist] = relationship("Artist", back_populates="followers")
